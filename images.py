from pygame.transform import scale
from constants import TILE_SIZE
from pygame.image import load
from os.path import join
from exe import pathof
from os import listdir
import pygame

pygame.display.set_mode((1, 1))

TILE_DIR = "assets/textures/tiles"
TILE_IMGS = {image[:-4]: scale(load(pathof(join(TILE_DIR, image))), (TILE_SIZE, TILE_SIZE)).convert() for image in listdir(TILE_DIR)}

SOLDIER1_IMG = pygame.image.load("assets/textures/soldier1_gun.png").convert_alpha()
SOLDIER2_IMG = pygame.image.load("assets/textures/soldier2_gun.png").convert_alpha()
BULLET_IMG = pygame.image.load("assets/textures/bullet.png").convert_alpha()

pygame.display.quit()