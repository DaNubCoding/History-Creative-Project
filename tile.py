from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from constants import TILE_SIZE, VEC, WIDTH, HEIGHT
from sprite import Sprite, LayersEnum
from random import randint, choice
from images import TILE_IMGS
import pygame

class TileManager:
    def __init__(self, manager: GameManager) -> None:
        self.manager = manager
        self.scene = self.manager.scene
        self.tiles = {}

    def generate(self, pos: tuple[int, int]):
        pos = VEC(pos)
        if pos.x == 10:
            return "trench1"
        return "ground" + str(randint(1, 2))

    def update(self):
        if LayersEnum.TILES.value not in self.scene.sprite_manager.layers:
            self.scene.sprite_manager.layers[LayersEnum.TILES.value] = []
        for tile in self.scene.sprite_manager.layers[LayersEnum.TILES.value]:
            self.scene.sprite_manager.remove(tile)
        camera = self.scene.player.camera
        tiles_start = VEC((camera.offset.x) // TILE_SIZE, (camera.offset.y) // TILE_SIZE)
        tiles_end = VEC((camera.offset.x + WIDTH) // TILE_SIZE + 1, (camera.offset.y + HEIGHT) // TILE_SIZE + 1)
        for x in range(int(tiles_start.x), int(tiles_end.x)):
            for y in range(int(tiles_start.y), int(tiles_end.y)):
                if (pos := (x, y)) not in self.tiles:
                    self.tiles[pos] = Tile(self.manager, pos, self.generate(pos))
                self.scene.sprite_manager.add(self.tiles[pos])

class Tile(Sprite):
    def __init__(self, manager: GameManager, pos: tuple[int, int], name: str) -> None:
        super().__init__(manager, LayersEnum.TILES)
        self.pos = VEC(pos) * TILE_SIZE
        self.name = name
        match self.name[:-1]:
            case "ground": self.rotation = choice([0, 90, 180, 270])
            case "trench": self.rotation = choice([0, 180])
        self.image = pygame.transform.rotate(TILE_IMGS[self.name], self.rotation)

    def update(self):
        pass

    def draw(self):
        self.manager.screen.blit(self.image, self.pos - self.scene.player.camera.offset)