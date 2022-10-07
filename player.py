from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from constants import WIDTH, HEIGHT, VEC, SCR_DIM
from sprite import Sprite, LayersEnum
from math import atan2, degrees
from images import SOLDIER_IMG
from pygame.locals import *
from utils import intvec
import pygame

class Camera(pygame.sprite.Sprite):
    def __init__(self, master):
        self.master = master
        self.actual_offset = self.master.size / 2
        self.actual_offset = self.master.pos - self.actual_offset - VEC(SCR_DIM) / 2 + self.master.size / 2
        self.offset = intvec(self.actual_offset)

    def update(self):
        tick_offset = self.master.pos - self.offset - VEC(SCR_DIM) / 2 + self.master.size / 2
        if -1 < tick_offset.x < 1:
            tick_offset.x = 0
        if -1 < tick_offset.y < 1:
            tick_offset.y = 0
        self.actual_offset += tick_offset / 10
        self.offset = intvec(self.actual_offset)

class Player(Sprite):
    def __init__(self, manager: GameManager) -> None:
        super().__init__(manager, LayersEnum.PLAYER)
        self.size = VEC(SOLDIER_IMG.get_size())
        self.pos = VEC(WIDTH // 2, HEIGHT // 2)
        self.camera = Camera(self)
        self.vel = VEC(0, 0)
        self.acc = VEC(0, 0)
        self.rot = 0
        self.image = SOLDIER_IMG
        
        self.CONST_ACC = 1200
        self.MAX_VEL = 240

    def update(self):
        keys = pygame.key.get_pressed()
        self.acc = VEC(0, 0)
        if keys[K_w]:
            self.acc.y -= 1
        if keys[K_s]:
            self.acc.y += 1
        if keys[K_a]:
            self.acc.x -= 1
        if keys[K_d]:
            self.acc.x += 1
        self.acc = (self.acc.normalize() if self.acc else VEC()) * self.CONST_ACC
        self.acc -= self.vel * 0.4 * self.CONST_ACC * self.manager.dt

        self.vel += intvec(self.acc) * self.manager.dt
        self.vel = self.vel.normalize() * self.MAX_VEL if self.vel.length() > self.MAX_VEL else self.vel
        self.pos += self.vel * self.manager.dt

        m_pos = VEC(pygame.mouse.get_pos())
        self.rot = degrees(atan2(m_pos.x - self.pos.x, m_pos.y - self.pos.y)) - 90

    def draw(self):
        self.image = pygame.transform.rotate(SOLDIER_IMG, self.rot)
        self.manager.screen.blit(self.image, self.pos - VEC(self.image.get_size()) // 2 + VEC(10, 0).rotate(-self.rot) - self.camera.offset)