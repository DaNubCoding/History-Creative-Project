from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from sprite import Sprite, LayersEnum
from constants import TILE_SIZE, VEC
from images import TILE_IMGS

class Tile(Sprite):
    def __init__(self, manager: GameManager, pos: tuple[int, int], name: str) -> None:
        super().__init__(manager, LayersEnum.TILES)
        self.pos = VEC(pos)
        self.name = name
        self.image = TILE_IMGS[self.name]

    def update(self):
        pass

    def draw(self):
        self.manager.screen.blit(self.image, self.pos - self.manager.scene.player.camera.offset)