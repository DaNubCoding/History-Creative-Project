from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from sprite import Sprite, LayersEnum
from constants import SCR_DIM, VEC
from images import PARCHMENT_IMG

class Notice(Sprite):
    def __init__(self, manager: GameManager) -> None:
        super().__init__(manager, LayersEnum.HUD)
        self.text = "Experiment Text, replace this!"

    def draw(self) -> None:
        self.manager.screen.blit(PARCHMENT_IMG, VEC(SCR_DIM) // 2 - VEC(PARCHMENT_IMG.get_size()) // 2)