from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from random import uniform, choice, choices, randint
from sprite import Sprite, LayersEnum
from constants import VEC, TILE_SIZE
from utils import intvec, inttup
from images import SOLDIER1_IMG1
from math import degrees, atan2
from bullet import PlayerBullet
from clamps import snap, clamp
from particles import Blood
from numpy import average
from enemy import Skull
from utils import sign
import pygame
import time

class Ally(Sprite):
    def __init__(self, manager: GameManager, pos: tuple[int, int]) -> None:
        super().__init__(manager, LayersEnum.ENEMIES)
        self.manager.scene.allies.append(self)
        self.pos = VEC(pos)
        self.vel = VEC(0, 0)
        self.acc = VEC(0, 0)
        self.coords = self.pos // TILE_SIZE
        self.rot = 0
        self.rot_target = 0
        self.max_speed = 140
        self.on_tile = None
        self.moving = False
        self.move_timer = time.time()
        self.move_interval = uniform(0.5, 1.5)
        self.move_duration = uniform(1, 4)
        self.move_direction = choice([VEC(-1, 0), VEC(1, 0), VEC(0, -1), VEC(0, 1), VEC(-1, -1), VEC(-1, 1), VEC(1, -1), VEC(1, 1)])
        self.fire_timer = time.time()
        self.fire_interval = uniform(2, 5)
        self.health = {
            "head": 100,
            "body": 100,
            "arms": 100,
            "legs": 100,
            "feet": 100
        }
        self.health_average = 100
        self.deviation = 10
        self.heavily_injured = False
        self.run_away = False
        self.target = None
        self.target_timer = time.time()
        self.target_interval = uniform(3, 6)

        self.CONST_ACC = 1000
        self.ROT_ACC = 3

    def update(self):
        if self.scene.player.pos.distance_to(self.pos) > 240:
            self.move_direction = VEC(sign(self.scene.player.pos.x - self.pos.x), sign(self.scene.player.pos.y - self.pos.y))
        else:
            if time.time() - self.move_timer > self.move_interval:
                self.move_interval = uniform(0.5, 1.5)
                self.move_timer = time.time()
                self.moving = True
                self.move_direction = choice([VEC(1, 0), VEC(1, -1), VEC(1, 1)])
            if self.moving and time.time() - self.move_timer > self.move_duration:
                self.move_duration = uniform(1, 4)
                self.move_timer = time.time()
                self.moving = False
                self.move_direction = VEC(0, 0)
            # if self.on_tile and self.on_tile.name[:-1] == "trench":
            #     self.move_direction = VEC(0, 0)

        if time.time() - self.target_timer > self.target_interval:
            self.target_timer = time.time()
            self.target_interval = uniform(3, 6)
            if self.scene.enemies:
                current = self.scene.enemies[0]
                for ally in self.scene.enemies:
                    if ally.pos.distance_to(self.pos) < current.pos.distance_to(self.pos):
                        current = ally
                self.target = current

        if time.time() - self.fire_timer > self.fire_interval and self.target:
            self.move_duration = 0
            self.rot_to_target()
            if abs(self.rot - self.rot_target) < 3:
                self.fire_timer = time.time()
                self.fire_interval = uniform(1, 4)
                PlayerBullet(self.manager, self, self.pos + VEC(10, -34).rotate(-self.rot))

        # if self.run_away and self.on_tile.name[:-1] != "trench":
        #     self.rot_to_target()
        #     self.move_direction = VEC(-sign(self.scene.player.pos.x - self.pos.x), 0)

        # Update acceleration
        self.acc = VEC(0, 0)
        self.acc = self.move_direction.copy()
        self.acc = self.acc.normalize() * self.CONST_ACC if self.acc else VEC()
        self.acc -= self.vel * 5
        
        for ally in self.scene.allies:
            if ally is self or self.pos.distance_to(ally.pos) > 30: continue
            self.acc += ((self.pos - ally.pos).normalize() if self.pos - ally.pos else VEC()) * 400

        # Update velocity
        self.vel += intvec(self.acc) * self.manager.dt
        if self.on_tile and self.on_tile.name[:-1] == "trench":
            self.vel -= self.vel * 20 * self.manager.dt
            self.health["feet"] -= 2 * self.manager.dt
            self.health["legs"] -= 1 * self.manager.dt
        self.vel = snap(self.vel, VEC(), VEC(1, 1))

        # Update position
        self.pos += intvec(self.vel) * self.manager.dt
        self.pos, _ = clamp(self.pos, VEC(-100, -600), VEC(4000, 600))
        self.coords = self.pos // TILE_SIZE

        # Update rotation
        self.rot_target = self.vel.angle_to(VEC(0, -1)) if self.vel else self.rot_target
        self.rot %= 360
        self.rot_target %= 360
        if abs((rot_diff := self.rot_target - self.rot)) < 180:
            self.rot += (self.rot_target - self.rot) * self.ROT_ACC * self.manager.dt
        else:
            self.rot -= sign(rot_diff) * (360 - abs(rot_diff)) * self.ROT_ACC * self.manager.dt
        self.rot = snap(self.rot, self.rot_target, 1)

        # Find the tile the player is on
        if inttup(self.coords) in self.scene.tile_manager.tiles:
            self.on_tile = self.scene.tile_manager.tiles[inttup(self.coords)]

        # Clamp health
        for part in self.health:
            if self.health[part] < 0:
                self.health[part] = 0
                if part in {"head", "body"}:
                    self.kill()
            elif self.health[part] < 30:
                self.heavily_injured = True

        # Losing blood
        if self.heavily_injured:
            for part in self.health:
                self.health[part] -= 0.005

        self.health_average = average(list(self.health.values()), weights=[16, 12, 2, 2, 2])
        if self.health_average < 75 or self.heavily_injured:
            self.run_away = True
        if self.health_average < 50:
            self.kill()

    def draw(self):
        self.image = pygame.transform.rotate(SOLDIER1_IMG1, self.rot)
        self.manager.screen.blit(self.image, self.pos - VEC(self.image.get_size()) // 2 + VEC(0, -10).rotate(-self.rot) - self.scene.player.camera.offset)
        # pygame.draw.circle(self.manager.screen, (0, 255, 0), self.pos - self.scene.player.camera.offset, 20, 3)

    def kill(self) -> None:
        Skull(self.manager, self.pos)
        try:
            self.scene.allies.remove(self)
        except ValueError:
            pass
        super().kill()

    def get_shot(self):
        self.health[choices(["head", "body", "arms", "legs"], weights=[3, 10, 6, 8])[0]] -= randint(40, 80)
        for _ in range(randint(20, 35)):
            Blood(self.manager, self.pos)

    def rot_to_target(self):
        if self.target:
            self.rot_target = degrees(atan2(self.target.pos.x - self.pos.x, self.target.pos.y - self.pos.y)) + 180