from pygame.math import Vector2
from pygame.locals import *
from exe import pathof
import pygame

VEC = Vector2
FPS = float("inf")
WIDTH, HEIGHT = SCR_DIM = 1000, 600
TILE_SIZE = 64

pygame.font.init()
FONT_FILE = pathof("assets/fonts/CfCrackAndBoldRegular-3jxp.ttf")
NOTICE_FONT = pygame.font.Font(FONT_FILE, 32)
NOTICE_SUB_FONT = pygame.font.Font(FONT_FILE, 16)
BIG_FONT = pygame.font.Font(FONT_FILE, 64)