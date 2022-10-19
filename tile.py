from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from constants import TILE_SIZE, VEC, WIDTH, HEIGHT
from images import TILE_IMGS, FLAG_IMG
from sprite import Sprite, LayersEnum
from random import randint, choice
from enemy import Enemy
import pygame

class TileManager:
    def __init__(self, manager: GameManager) -> None:
        self.manager = manager
        self.scene = self.manager.scene
        self.tiles = {}
        self.trench_positions = {}
        self.scene.sprite_manager.layers[LayersEnum.TILES.value] = []
        for x in range(-2, 50):
            for y in range(-10, 11):
                self.tiles[(x, y)] = Tile(self.manager, (x, y), self.generate((x, y)))

    def generate(self, pos: tuple[int, int]):
        pos = VEC(pos)
        if pos.x not in self.trench_positions:
            self.trench_positions[pos.x] = not randint(0, 10) or pos.x % 16 == 0
        if pos.x >= 0 and (self.trench_positions[pos.x] or pos.x == 0):
            if (randint(0, 7) == 0 or pos.y % 10 == 0) and 8 < pos.x <= 50 and -10 < pos.y <= 10:
                Enemy(self.manager, pos * TILE_SIZE + (randint(16, 48), randint(16, 48)))
            return "trench1"
        if randint(0, 60) == 0 and 8 < pos.x <= 50 and -10 < pos.y <= 10:
            Enemy(self.manager, pos * TILE_SIZE + (randint(16, 48), randint(16, 48)))
        return "ground" + (str(randint(1, 3)) if randint(0, 16) else str(randint(4, 7)))

    def update(self):
        for tile in self.scene.sprite_manager.layers[LayersEnum.TILES.value]:
            self.scene.sprite_manager.remove(tile)
        camera = self.scene.player.camera
        tiles_start = VEC((camera.offset.x) // TILE_SIZE, (camera.offset.y) // TILE_SIZE)
        tiles_end = VEC((camera.offset.x + WIDTH) // TILE_SIZE + 1, (camera.offset.y + HEIGHT) // TILE_SIZE + 1)
        for x in range(int(tiles_start.x), int(tiles_end.x)):
            for y in range(int(tiles_start.y), int(tiles_end.y)):
                if (pos := (x, y)) not in self.tiles:
                    self.tiles[pos] = Tile(self.manager, pos, self.generate(pos))
                self.scene.sprite_manager.add(self.tiles[(x, y)])

class Tile(Sprite):
    def __init__(self, manager: GameManager, pos: tuple[int, int], name: str) -> None:
        super().__init__(manager, LayersEnum.TILES)
        self.pos = VEC(pos) * TILE_SIZE
        self.name = name
        match self.name[:-1]:
            case "ground": self.rotation = choice([0, 90, 180, 270])
            case "trench": self.rotation = choice([0, 180])
        self.image = pygame.transform.rotate(TILE_IMGS[self.name], self.rotation)
        self.flag = pos[0] == 50 and randint(0, 4)
        self.flag_offset = VEC(randint(16, 48), randint(16, 48))

    def update(self):
        pass

    def draw(self):
        self.manager.screen.blit(self.image, self.pos - self.scene.player.camera.offset)
        if self.flag:
            self.manager.screen.blit(FLAG_IMG, self.pos + self.flag_offset - self.scene.player.camera.offset)