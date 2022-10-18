from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from sprite import Sprite, LayersEnum
from random import randint, uniform
from constants import VEC
from utils import intvec
import pygame
import time

class Blood(Sprite):
    def __init__(self, manager: GameManager, pos: tuple[int, int]) -> None:
        super().__init__(manager, LayersEnum.PARTICLES)
        self.pos = VEC(pos)
        self.vel = VEC(randint(-250, 250), randint(-250, 250))
        self.acc = VEC(0, 0)
        self.radius = randint(1, 4)
        self.timer = time.time()
        self.alive_time = uniform(0.5, 1)

    def update(self) -> None:
        self.acc = -self.vel * 7
        self.vel += intvec(self.acc) * self.manager.dt
        self.pos += intvec(self.vel) * self.manager.dt
        # if time.time() - self.timer > self.alive_time:
        #     self.kill()

    def draw(self) -> None:
        pygame.draw.circle(self.manager.screen, (140, 0, 0), self.pos - self.scene.player.camera.offset, self.radius)