from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from constants import TILE_SIZE, WIDTH, HEIGHT, VEC, SCR_DIM
from sprite import Sprite, LayersEnum
from utils import intvec, inttup
from math import atan2, degrees
from images import SOLDIER_IMG
from pygame.locals import *
from bullet import Bullet
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
        self.size = VEC(SOLDIER_IMG.get_size())
        self.pos = VEC(WIDTH // 2, HEIGHT // 2)
        self.coords = self.pos // TILE_SIZE
        self.camera = Camera(self)
        self.vel = VEC(0, 0)
        self.acc = VEC(0, 0)
        self.rot = 0
        self.image = SOLDIER_IMG
        self.bullet_timer = time.time()
        self.on_tile = None
        
        self.CONST_ACC = 1000
        self.MAX_VEL = 240

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
        self.vel = self.vel.normalize() * self.MAX_VEL if self.vel.length() > self.MAX_VEL else self.vel
        if self.on_tile and self.on_tile.name[:-1] == "trench":
            self.vel -= self.vel * 0.05

        # Update position
        self.pos += self.vel * self.manager.dt
        self.coords = self.pos // TILE_SIZE

        # Update rotation
        self.rot = degrees(atan2(m_pos.x - self.pos.x + self.camera.offset.x, m_pos.y - self.pos.y + self.camera.offset.y)) - 90

        self.camera.update()

        # Find the tile the player is on
        if inttup(self.coords) in self.scene.tile_manager.tiles:
            self.on_tile = self.scene.tile_manager.tiles[inttup(self.coords)]

        # Spawn bullets
        if keys[K_SPACE] and time.time() - self.bullet_timer > 2:
            Bullet(self.manager, self.pos + VEC(34, 10).rotate(-self.rot)) # Offset to the gun on player's image
            self.bullet_timer = time.time()

    def draw(self):
        self.image = pygame.transform.rotate(SOLDIER_IMG, self.rot)
        self.manager.screen.blit(self.image, self.pos - VEC(self.image.get_size()) // 2 + VEC(10, 0).rotate(-self.rot) - self.camera.offset)
