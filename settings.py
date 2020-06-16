import random
import pygame as pg
vec = pg.math.Vector2

true = True
false = False
null = None
none = None
Null = None

#colors
c1 = (25,25,25)
c10 = (250,250,250)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
LIME = (0, 255, 0)
GREEN = (0, 128, 0)
DARKGREEN = (0, 64, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100,100,255)


HEIGHT = 720
WIDTH = 1056
SIZE = (WIDTH, HEIGHT)

TILESIZE = 48

TILEWIDTH = int(WIDTH / TILESIZE)
TILEHEIGHT = int(HEIGHT / TILESIZE)

FPS = 120

MAXSEEDS = 100
seedgen=random.randint(-MAXSEEDS, MAXSEEDS)
ammount = 5
MAPSIZEX = 64
MAPSIZEY = 64
CHUNKSIZE = 4
CHUNKTILESIZE = CHUNKSIZE * TILESIZE
CHUNKRENDER = 2
CHUNKRENDERX = 3
CHUNKRENDERY = 3
XLIMIT = 2 * CHUNKTILESIZE
YLIMIT = 2 * CHUNKTILESIZE
savetimer = 1000

# Player settings
PLAYER_SPEED = 250
PLAYER_DEFAULT_SPAWN = (100, 100)
PLAYER_HITRECT = pg.Rect(TILESIZE, TILESIZE, 32, 24)
PLAYER_COLLIDE = false

#layers
PLAYER_LAYER = 3
ITEM_LAYER = 2



# Item settings
BOB_RANGE = 16
BOB_SPEED = 0.8
MAXITEMS = 24



# Colliding function

def collide_hit_rect(one, two):
	return one.hit_rect.colliderect(two.rect)


# UI settings
UI_MARGIN = 10
