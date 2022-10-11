from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from random import uniform, choice, choices, randint
from images import SOLDIER2_IMG, SKULL_IMG
from sprite import Sprite, LayersEnum
from constants import VEC, TILE_SIZE
from utils import intvec, inttup
from math import degrees, atan2
from bullet import EnemyBullet
from particles import Blood
from numpy import average
from clamps import snap
from utils import sign
import pygame
import time

class Enemy(Sprite):
    def __init__(self, manager: GameManager, pos: tuple[int, int]) -> None:
        super().__init__(manager, LayersEnum.ENEMIES)
        self.manager.scene.enemies.append(self)
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
        self.move_interval = uniform(0.5, 3)
        self.move_duration = uniform(1, 4)
        self.move_direction = choice([VEC(-1, 0), VEC(1, 0), VEC(0, -1), VEC(0, 1), VEC(-1, -1), VEC(-1, 1), VEC(1, -1), VEC(1, 1)])
        self.fire_timer = time.time()
        self.fire_interval = uniform(2, 6)
        self.health = {
            "head": 100,
            "body": 100,
            "arms": 100,
            "legs": 100,
            "feet": 100
        }
        self.health_average = 100
        self.deviation = 10

        self.NORMAL_MAX_SPEED = 140
        self.CONST_ACC = 1000
        self.ROT_ACC = 3

    def update(self):
        if time.time() - self.move_timer > self.move_interval:
            self.move_interval = uniform(0.5, 3)
            self.move_timer = time.time()
            self.moving = True
            self.move_direction = choice([VEC(-1, 0), VEC(1, 0), VEC(0, -1), VEC(0, 1), VEC(-1, -1), VEC(-1, 1), VEC(1, -1), VEC(1, 1)])
        if self.moving and time.time() - self.move_timer > self.move_duration:
            self.move_duration = uniform(1, 4)
            self.move_timer = time.time()
            self.moving = False
            self.move_direction = VEC(0, 0)

        if time.time() - self.fire_timer > self.fire_interval:
            self.move_duration = 0
            self.rot_target = degrees(atan2(self.scene.player.pos.x - self.pos.x, self.scene.player.pos.y - self.pos.y)) + 180
            if abs(self.rot - self.rot_target) < 3:
                self.fire_timer = time.time()
                self.fire_interval = uniform(2, 6)
                EnemyBullet(self.manager, self, self.pos + VEC(10, -34).rotate(-self.rot))

        # Update acceleration
        self.acc = VEC(0, 0)
        self.acc = self.move_direction.copy()
        self.acc = self.acc.normalize() * self.CONST_ACC if self.acc else VEC()
        self.acc -= self.vel * 5

        # Update velocity
        self.vel += intvec(self.acc) * self.manager.dt
        self.vel = self.vel.normalize() * self.max_speed if self.vel.length() > self.max_speed else self.vel
        if self.on_tile and self.on_tile.name[:-1] == "trench":
            self.vel -= self.vel * 0.05
            self.health["feet"] -= 0.0025
            self.max_speed = (self.NORMAL_MAX_SPEED - 30) * self.health["feet"] / 100 + 30
        self.vel = snap(self.vel, VEC(), VEC(1, 1))

        # Update position
        self.pos += intvec(self.vel) * self.manager.dt
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
        self.health_average = average(list(self.health.values()), weights=[16, 12, 2, 2, 2])
        if self.health_average < 60:
            self.kill()

    def draw(self):
        self.image = pygame.transform.rotate(SOLDIER2_IMG, self.rot)
        self.manager.screen.blit(self.image, self.pos - VEC(self.image.get_size()) // 2 + VEC(0, -10).rotate(-self.rot) - self.scene.player.camera.offset)
        # pygame.draw.circle(self.manager.screen, (0, 255, 0), self.pos - self.scene.player.camera.offset, 20, 3)

    def kill(self) -> None:
        Skull(self.manager, self.pos)
        try:
            self.scene.enemies.remove(self)
        except ValueError:
            pass
        super().kill()

    def get_shot(self):
        self.health[choices(["head", "body", "arms", "legs"], weights=[3, 10, 6, 8])[0]] -= randint(40, 80)
        for _ in range(randint(20, 35)):
            Blood(self.manager, self.pos)

class Skull(Sprite):
    def __init__(self, manager: GameManager, pos: tuple[int, int]) -> None:
        super().__init__(manager, LayersEnum.ENEMIES)
        self.pos = VEC(pos)

    def draw(self):
        self.manager.screen.blit(SKULL_IMG, self.pos - VEC(SKULL_IMG.get_size()) // 2 - self.scene.player.camera.offset)