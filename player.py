from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from constants import WIDTH, HEIGHT, VEC, SCR_DIM
from sprite import Sprite, LayersEnum
from images import SOLDIER_IMG
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

    def update(self):
        self.vel += self.acc * self.manager.dt
        self.pos += self.vel * self.manager.dt

    def draw(self):
        self.manager.screen.blit(SOLDIER_IMG, self.pos - self.camera.offset)