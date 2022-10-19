from pygame.transform import scale, smoothscale
from constants import TILE_SIZE, VEC
from pygame.image import load
from os.path import join
from exe import pathof
from os import listdir
import pygame

pygame.display.set_mode((1, 1))

TILE_DIR = "assets/textures/tiles"
TILE_IMGS = {image[:-4]: scale(load(pathof(join(TILE_DIR, image))), (TILE_SIZE, TILE_SIZE)).convert() for image in listdir(TILE_DIR)}

ITEM_DIR = "assets/textures/items"
ITEM_IMGS = {image[:-4]: load(pathof(join(ITEM_DIR, image))).convert_alpha() for image in listdir(ITEM_DIR)}

SOLDIER1_IMG1 = pygame.image.load(pathof("assets/textures/soldier1_ross.png")).convert_alpha()
SOLDIER1_IMG2 = pygame.image.load(pathof("assets/textures/soldier1_enfield.png")).convert_alpha()
SOLDIER2_IMG = pygame.image.load(pathof("assets/textures/soldier2_gun.png")).convert_alpha()
BULLET_IMG = pygame.image.load(pathof("assets/textures/bullet.png")).convert_alpha()
SKULL_IMG = pygame.image.load(pathof("assets/textures/skull.png")).convert_alpha()
PARCHMENT_IMG = pygame.image.load(pathof("assets/textures/parchment.png")).convert_alpha()
FLAG_IMG = pygame.image.load(pathof("assets/textures/flag.png")).convert_alpha()

pygame.display.quit()