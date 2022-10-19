from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from constants import SCR_DIM, VEC, NOTICE_FONT, NOTICE_SUB_FONT
from sprite import Sprite, LayersEnum
from pygame.locals import SRCALPHA
from images import PARCHMENT_IMG
from textwrap import wrap
import pygame

class Notice(Sprite):
    def __init__(self, manager: GameManager, text: str = "Experiment Text, replace this!", sub_text: str = "") -> None:
        super().__init__(manager, LayersEnum.HUD)
        self.text = wrap(text, 36)
        self.text_surfs = [NOTICE_FONT.render(line, True, (0, 0, 0)) for line in self.text]
        self.text_surf = pygame.Surface(PARCHMENT_IMG.get_size(), SRCALPHA)
        y = -80
        for surf in self.text_surfs:
            self.text_surf.blit(surf, (VEC(PARCHMENT_IMG.get_size()) // 2 - VEC(surf.get_size()) // 2 + VEC(0, y)))
            y += NOTICE_FONT.get_height()
        surf = NOTICE_SUB_FONT.render(sub_text, True, (0, 0, 0))
        self.text_surf.blit(surf, (VEC(PARCHMENT_IMG.get_size()) // 2 - VEC(surf.get_size()) // 2 + VEC(0, 90)))

    def draw(self) -> None:
        self.manager.screen.blit(PARCHMENT_IMG, VEC(SCR_DIM) // 2 - VEC(PARCHMENT_IMG.get_size()) // 2)
        self.manager.screen.blit(self.text_surf, VEC(SCR_DIM) // 2 - VEC(PARCHMENT_IMG.get_size()) // 2)