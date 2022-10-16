from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from constants import SCR_DIM, TILE_SIZE, VEC
from utils import intvec, inttup, sign
from sprite import LayersEnum, Sprite
from random import choices, randint
from math import atan2, degrees
from images import SOLDIER1_IMG
from bullet import PlayerBullet
from particles import Blood
from pygame.locals import *
from numpy import average
from clamps import snap
import pygame
import time

class Camera:
    def __init__(self, master: Player):
        self.master = master
        self.manager = self.master.manager
        self.actual_offset = self.master.size / 2
        self.actual_offset = self.master.pos - self.actual_offset - VEC(SCR_DIM) / 2
        self.offset = intvec(self.actual_offset)

    def update(self):
        tick_offset = self.master.pos - self.offset - VEC(SCR_DIM) / 2
        if -1 < tick_offset.x < 1:
            tick_offset.x = 0
        if -1 < tick_offset.y < 1:
            tick_offset.y = 0
        self.actual_offset += tick_offset * 5 * self.manager.dt
        self.offset = intvec(self.actual_offset)

class Player(Sprite):
    def __init__(self, manager: GameManager) -> None:
        super().__init__(manager, LayersEnum.PLAYER)
        self.size = VEC(SOLDIER1_IMG.get_size())
        self.pos = VEC(TILE_SIZE // 2, 0)
        self.coords = self.pos // TILE_SIZE
        self.camera = Camera(self)
        self.vel = VEC(0, 0)
        self.acc = VEC(0, 0)
        self.rot = 10
        self.rot_target = 0
        self.image = SOLDIER1_IMG
        self.bullet_timer = time.time()
        self.on_tile = None
        self.max_speed = 220
        self.health = {
            "head": 100,
            "body": 100,
            "arms": 100,
            "legs": 100,
            "feet": 100
        }
        self.health_average = 100
        self.deviation = 10
        self.bullets = 20
        self.heavily_injured = False

        self.NORMAL_MAX_SPEED = 220
        self.CONST_ACC = 1000
        self.ROT_ACC = 5

    def update(self):
        keys = pygame.key.get_pressed()
        m_pos = VEC(pygame.mouse.get_pos())

        # Update acceleration
        self.acc = VEC(0, 0)
        if keys[K_w]: self.acc.y -= 1
        if keys[K_s]: self.acc.y += 1
        if keys[K_a]: self.acc.x -= 1
        if keys[K_d]: self.acc.x += 1
        self.acc = self.acc.normalize() * self.CONST_ACC if self.acc else VEC()
        self.acc -= self.vel * 5

        # Update velocity
        self.vel += intvec(self.acc) * self.manager.dt
        self.vel = self.vel.normalize() * self.max_speed if self.vel.length() > self.max_speed else self.vel
        if self.on_tile and self.on_tile.name[:-1] == "trench":
            self.vel -= self.vel * 0.05
            self.health["feet"] -= 0.004
            self.health["legs"] -= 0.002
            self.max_speed = (self.NORMAL_MAX_SPEED - 30) * (self.health["feet"] + self.health["legs"]) / 200 + 30
        self.vel = snap(self.vel, VEC(), VEC(1, 1))

        # Update position
        self.pos += intvec(self.vel) * self.manager.dt
        self.coords = self.pos // TILE_SIZE

        # Update rotation
        self.rot_target = degrees(atan2(m_pos.x - self.pos.x + self.camera.offset.x, m_pos.y - self.pos.y + self.camera.offset.y)) - 180
        self.rot %= 360
        self.rot_target %= 360
        if abs(rot_diff := self.rot_target - self.rot) < 180:
            self.rot += (self.rot_target - self.rot) * self.ROT_ACC * self.manager.dt
        else:
            self.rot -= sign(rot_diff) * (360 - abs(rot_diff)) * self.ROT_ACC * self.manager.dt
        self.rot = snap(self.rot, self.rot_target, 1)

        # Update camera
        self.camera.update()

        # Find the tile the player is on
        if inttup(self.coords) in self.scene.tile_manager.tiles:
            self.on_tile = self.scene.tile_manager.tiles[inttup(self.coords)]

        # Spawn bullets
        if keys[K_SPACE] and time.time() - self.bullet_timer > 2:
            PlayerBullet(self.manager, self, self.pos + VEC(10, -34).rotate(-self.rot)) # Offset to the gun on player's image
            self.bullet_timer = time.time()

        # Update health
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
        if self.health_average < 60:
            try:
                self.kill()
            except:
                pass

    def draw(self):
        self.image = pygame.transform.rotate(SOLDIER1_IMG, self.rot)
        self.manager.screen.blit(self.image, self.pos - VEC(self.image.get_size()) // 2 + VEC(0, -10).rotate(-self.rot) - self.camera.offset)

    def get_shot(self):
        self.health[choices(["head", "body", "arms", "legs"], weights=[3, 10, 6, 8])[0]] -= randint(40, 80)
        for _ in range(randint(20, 35)):
            Blood(self.manager, self.pos)

class PlayerHealthHUD(Sprite):
    def __init__(self, manager: GameManager) -> None:
        super().__init__(manager, LayersEnum.HUD)
        self.health = self.scene.player.health
        self.image = pygame.Surface((50, 130), SRCALPHA)
        self.colors = {
            "head": (0, 255, 0),
            "body": (0, 255, 0),
            "arms": (0, 255, 0),
            "legs": (0, 255, 0),
            "feet": (0, 255, 0)
        }

    def update(self):
        self.colors = {
            "head": [round((100 - self.health["head"]) / 50 * 255) if self.health["head"] > 50 else 255, round(self.health["head"] / 50 * 255) if self.health["head"] <= 50 else 255, 0],
            "body": [round((100 - self.health["body"]) / 50 * 255) if self.health["body"] > 50 else 255, round(self.health["body"] / 50 * 255) if self.health["body"] <= 50 else 255, 0],
            "arms": [round((100 - self.health["arms"]) / 50 * 255) if self.health["arms"] > 50 else 255, round(self.health["arms"] / 50 * 255) if self.health["arms"] <= 50 else 255, 0],
            "legs": [round((100 - self.health["legs"]) / 50 * 255) if self.health["legs"] > 50 else 255, round(self.health["legs"] / 50 * 255) if self.health["legs"] <= 50 else 255, 0],
            "feet": [round((100 - self.health["feet"]) / 50 * 255) if self.health["feet"] > 50 else 255, round(self.health["feet"] / 50 * 255) if self.health["feet"] <= 50 else 255, 0],
        }
        for color in self.colors:
            for i, component in enumerate(self.colors[color]):
                if component < 0:
                    self.colors[color][i] = 0

    def draw(self):
        pygame.draw.circle(self.image, self.colors["head"], (25, 15), 15)
        pygame.draw.circle(self.image, (80, 80, 80), (25, 15), 15, 2)

        pygame.draw.rect(self.image, self.colors["body"], (10, 30, 30, 50))
        pygame.draw.rect(self.image, (80, 80, 80), (10, 30, 30, 50), 2)

        pygame.draw.rect(self.image, self.colors["arms"], (0, 30, 10, 50))
        pygame.draw.rect(self.image, (80, 80, 80), (0, 30, 10, 50), 2)

        pygame.draw.rect(self.image, self.colors["arms"], (40, 30, 10, 50))
        pygame.draw.rect(self.image, (80, 80, 80), (40, 30, 10, 50), 2)

        pygame.draw.rect(self.image, self.colors["legs"], (10, 80, 15, 40))
        pygame.draw.rect(self.image, (80, 80, 80), (10, 80, 15, 50), 2)

        pygame.draw.rect(self.image, self.colors["legs"], (25, 80, 15, 40))
        pygame.draw.rect(self.image, (80, 80, 80), (25, 80, 15, 50), 2)

        pygame.draw.rect(self.image, self.colors["feet"], (10, 120, 15, 10))
        pygame.draw.rect(self.image, (80, 80, 80), (10, 120, 15, 10), 2)

        pygame.draw.rect(self.image, self.colors["feet"], (25, 120, 15, 10))
        pygame.draw.rect(self.image, (80, 80, 80), (25, 120, 15, 10), 2)

        self.manager.screen.blit(self.image, (20, 20))
