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

GAME_STATES = {'onmenu' : 0, 'ingame' : 1, 'paused' : 2, 'gameover' : 3}

# Player settings
PLAYER_SPEED = 250
PLAYER_DEFAULT_SPAWN = (100000, 100000)
PLAYER_HITRECT = pg.Rect(TILESIZE, TILESIZE, 32, 24)
PLAYER_COLLIDE = false
PLAYER_DEFAULT_NAME = "Chris"

# World settings
MAXSEED = 10000000
seedgen=random.randint(-MAXSEED, MAXSEED)
ammount = 5
MAPSIZEX = 64
MAPSIZEY = 64
CHUNKSIZE = 4
CHUNKTILESIZE = CHUNKSIZE * TILESIZE
CHUNKRENDER = 3
DEFAULT_WORLD_NAME = 'EMPTY'
MAX_WORLD_NAME_LENGTH = 30

DEFAULT_WORLD_FORMAT = {
"world_name" : str(),
"seed" : int(),
"map" : dict(),
"player" : {
	"pos" : PLAYER_DEFAULT_SPAWN,
	"name" : PLAYER_DEFAULT_NAME,
	"selected_slot" : -1,
	"fullinv" : {
		0 : {"item": "empty", "count" : 1},
		1 : {"item": "empty", "count" : 1},
		2 : {"item": "empty", "count" : 1},
		3 : {"item": "empty", "count" : 1},
		4 : {"item": "empty", "count" : 1},
		5 : {"item": "empty", "count" : 1},
		6 : {"item": "empty", "count" : 1},
		7 : {"item": "empty", "count" : 1},
		8 : {"item": "empty", "count" : 1}
		}
	}
}

XLIMIT = 2 * CHUNKTILESIZE
YLIMIT = 2 * CHUNKTILESIZE
savetimer = 1000



#layers
PLAYER_LAYER = 3
ITEM_LAYER = 2



# Item settings
BOB_RANGE = 16
BOB_SPEED = 0.8
MAXITEMS = 24
ITEM_SPAWN_RATIO = 1



# Colliding function

def collide_hit_rect(one, two):
	return one.hit_rect.colliderect(two.rect)


# UI settings
UI_MARGIN = 10
