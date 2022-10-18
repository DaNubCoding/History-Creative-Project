from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from pygame.locals import KEYDOWN, K_RETURN
from notice import Notice
from scene import Scene

class MainMenu(Scene):
    def setup(self) -> None:
        super().setup()
        Notice(self.manager)

    def update(self) -> None:
        super().update()
        if KEYDOWN in self.manager.events:
            self.manager.new_scene(self.manager.Scenes.GAME)

    def draw(self) -> None:
        super().draw()

class GameOver(Scene):
    def __init__(self, manager: GameManager) -> None:
        super().__init__(manager)

    def setup(self, game: Scene = None) -> None:
        super().setup()
        self.game = game
        self.player = self.game.player
        self.allies = self.game.allies
        self.enemies = self.game.enemies
        Notice(self.manager)

    def update(self) -> None:
        super().update()
        self.game.update()
        if KEYDOWN in self.manager.events and self.manager.events[KEYDOWN].key == K_RETURN:
            self.manager.new_scene(self.manager.Scenes.GAME)

    def draw(self) -> None:
        self.game.draw()
        super().draw()