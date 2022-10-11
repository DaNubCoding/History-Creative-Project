from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from sprite import Sprite, LayersEnum
from images import BULLET_IMG
from random import randint
from constants import VEC
import pygame

class Bullet(Sprite):
    def __init__(self, manager: GameManager, master: Sprite, pos: tuple[int, int]) -> None:
        super().__init__(manager, LayersEnum.BULLETS)
        self.master = master
        self.pos = VEC(pos)
        self.deviation = randint(-master.deviation, master.deviation)
        self.vel = VEC(800, 0).rotate(-self.master.rot - 90 + self.deviation)
        self.image = pygame.transform.rotate(BULLET_IMG, self.master.rot + self.deviation)

    def update(self):
        self.pos += self.vel * self.manager.dt
        if self.pos.distance_to(self.scene.player.pos) > 800:
            self.kill()

    def draw(self):
        self.manager.screen.blit(self.image, self.pos - VEC(self.image.get_size()) // 2 - self.scene.player.camera.offset)