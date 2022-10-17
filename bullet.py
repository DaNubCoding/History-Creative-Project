from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager

from sprite import Sprite, LayersEnum
from images import BULLET_IMG
from random import randint
from constants import VEC
import pygame

class Bullet(Sprite):
    def __init__(self, manager: GameManager, master: Sprite, pos: tuple[int, int]) -> None:
        super().__init__(manager, LayersEnum.BULLETS)
        self.master = master
        self.pos = VEC(pos)
        self.deviation = randint(-master.deviation, master.deviation)
        # 15 accounts for the slight angle of the gun
        self.vel = VEC(800, 0).rotate(-self.master.rot - 90 - 15 + self.deviation)
        self.image = pygame.transform.rotate(BULLET_IMG, self.vel.angle_to(VEC(0, -1)))

    def update(self):
        self.pos += self.vel * self.manager.dt

        if self.pos.distance_to(self.scene.player.pos) > 800:
            self.kill()

    def draw(self):
        self.manager.screen.blit(self.image, self.pos - VEC(self.image.get_size()) // 2 - self.scene.player.camera.offset)

class PlayerBullet(Bullet):
    def __init__(self, manager: GameManager, master: Sprite, pos: tuple[int, int]) -> None:
        super().__init__(manager, master, pos)
        self.trench_hit = randint(0, 5) == 0

    def update(self):
        super().update()
        for enemy in self.scene.enemies:
            if self.pos.distance_to(enemy.pos) < 20 and (enemy.on_tile.name[:-1] != "trench" or self.trench_hit):
                enemy.get_shot()
                self.kill()

class EnemyBullet(Bullet):
    def __init__(self, manager: GameManager, master: Sprite, pos: tuple[int, int]) -> None:
        super().__init__(manager, master, pos)
        self.trench_hit = randint(0, 5) == 0
        self.vel = VEC(800, 0).rotate(-self.master.rot - 90 + self.deviation)

    def update(self):
        super().update()
        if self.pos.distance_to(self.scene.player.pos) < 20 and (self.scene.player.on_tile.name[:-1] != "trench" or self.trench_hit):
            self.scene.player.get_shot()
            self.kill()