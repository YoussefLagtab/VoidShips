import pygame as pg
import random
from settings import *
from textures import *

class Block(pg.sprite.Sprite):
	def __init__(self, game, x, y, type):
		self.groups = game.all_sprites, game.grass, game.floortiles
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.type = type
		self.image = TERRAIN[type]
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.pos = vec(x, y) * TILESIZE
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE
		self.tilepos = (int(self.pos.x / TILESIZE), int(self.pos.y / TILESIZE))
		self.chunkpos = (int(self.tilepos[0] / CHUNKSIZE), int(self.tilepos[1] / CHUNKSIZE))
		self.chunkrect = pg.Rect(self.rect.x, self.rect.y, CHUNKTILESIZE, CHUNKTILESIZE)
		n = random.randint(0, 3)
		if n == 0:
			self.image = pg.transform.flip(self.image, true, true)
		if n == 1:
			self.image = pg.transform.flip(self.image, false, true)
		if n == 2:
			self.image = pg.transform.flip(self.image, true, false)


	def change(self, type):
		print(self.type, type)
		self.type = type
		self.image = TERRAIN[type]
