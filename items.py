from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from sprite import Sprite, LayersEnum
from images import ITEM_IMGS
from random import randint
from constants import VEC
import pygame

class Item(Sprite):
    def __init__(self, manager: GameManager, pos: tuple[int, int], name: str) -> None:
        super().__init__(manager, LayersEnum.ITEMS)
        self.pos = VEC(pos)
        self.name = name
        self.image = pygame.transform.rotate(ITEM_IMGS[self.name], randint(0, 360))

    def update(self) -> None:
        if self.pos.distance_to(self.scene.player.pos) < 40:
            if self.name == "lee_enfield_rifle":
                self.scene.player.weapon_damage = 70
                self.scene.player.weapon = "enfield"
                self.scene.player.bullet_interval = 1
                self.scene.player.deviation = 5
                self.kill()
            elif self.name == "med_kit":
                for part in self.scene.player.health:
                    self.scene.player.health[part] += (100 - self.scene.player.health[part]) * 0.4
                    if self.scene.player.health[part] > 100:
                        self.scene.player.health[part] = 100
                self.scene.player.heavily_injured = False
                self.kill()

    def draw(self) -> None:
        self.manager.screen.blit(self.image, self.pos - VEC(self.image.get_size()) // 2 - self.scene.player.camera.offset)