from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from sprite import Sprite, LayersEnum
from images import BULLET_IMG
from constants import VEC
import pygame

class Bullet(Sprite):
    def __init__(self, manager: GameManager, pos: tuple[int, int]) -> None:
        super().__init__(manager, LayersEnum.BULLETS)
        self.pos = VEC(pos)
        self.vel = VEC(800, 0).rotate(-self.scene.player.rot)
        self.image = pygame.transform.rotate(BULLET_IMG, self.scene.player.rot - 90)

    def update(self):
        self.pos += self.vel * self.manager.dt
        if self.pos.distance_to(self.scene.player.pos) > 800:
            self.kill()

    def draw(self):
        self.manager.screen.blit(self.image, self.pos - VEC(self.image.get_size()) // 2 - self.scene.player.camera.offset)