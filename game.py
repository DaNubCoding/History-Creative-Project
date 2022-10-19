from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from constants import NOTICE_SUB_FONT, TILE_SIZE, VEC, BIG_FONT
from player import Player, PlayerHealthHUD
from tile import TileManager
from random import randint
from scene import Scene
from enemy import Enemy
from ally import Ally

class Game(Scene):
    def setup(self) -> None:
        # Main game initialization goes here
        super().setup()
        self.player = Player(self.manager)
        self.player_health_hud = PlayerHealthHUD(self.manager)
        self.enemies: list[Enemy] = []
        self.allies: list[Ally] = []
        self.tile_manager = TileManager(self.manager)
        for _ in range(len(self.enemies) // 3 + 2):
            Ally(self.manager, VEC(32, randint(-5, 5) * TILE_SIZE))

    def update(self) -> None:
        # Main game update logic goes here
        self.tile_manager.update()
        super().update()
        # or here if the logic should run after all sprites update

    def draw(self) -> None:
        # Main game drawing goes here
        self.manager.screen.fill((0, 0, 0))
        super().draw()
        self.manager.screen.blit(NOTICE_SUB_FONT.render("German Soldiers Left:", True, (0, 0, 0)), (20, 20))
        self.manager.screen.blit(BIG_FONT.render(f"{len(self.enemies)}", True, (0, 0, 0)), (20, 36))
        # or here if drawn on top of all sprites