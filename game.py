from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from player import Player, PlayerHealthHUD
from constants import TILE_SIZE, VEC
from tile import TileManager
from random import randint
from scene import Scene
from enemy import Enemy

class Game(Scene):
    def setup(self) -> None:
        # Main game initialization goes here
        super().setup()
        self.player = Player(self.manager)
        self.tile_manager = TileManager(self.manager)
        self.player_health_hud = PlayerHealthHUD(self.manager)
        self.enemies: list[Enemy] = []

    def update(self) -> None:
        # Main game update logic goes here
        self.tile_manager.update()
        super().update()
        # or here if the logic should run after all sprites update

    def draw(self) -> None:
        # Main game drawing goes here
        self.manager.screen.fill((0, 0, 0))
        super().draw()
        # or here if drawn on top of all sprites