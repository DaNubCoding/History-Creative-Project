from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from pygame.locals import KEYDOWN
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