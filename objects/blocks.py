import pygame as pg
import random
from settings import *
from textures import *

class Block(pg.sprite.Sprite):
	def __init__(self, game, x, y, type):
		self.groups = game.all_sprites, game.grass, game.floortiles
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = TERRAIN[type]
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.pos = vec(x, y) * TILESIZE
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE
		self.tilepos = vec(int(self.pos.x / TILESIZE), int(self.pos.y / TILESIZE))
		self.chunkpos = vec(int(self.tilepos.x / CHUNKSIZE), int(self.tilepos.y / CHUNKSIZE))
		self.chunkrect = pg.Rect(self.rect.x, self.rect.y, CHUNKTILESIZE, CHUNKTILESIZE)
		n = random.randint(0, 3)
		if n == 0:
			self.image = pg.transform.flip(self.image, true, true)
		if n == 1:
			self.image = pg.transform.flip(self.image, false, true)
		if n == 2:
			self.image = pg.transform.flip(self.image, true, false)

class Void(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.collidables, game.void
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		num = random.randint(0,3)
		self.original_image = VOID[num]
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE
		self.pos = vec(x, y) * TILESIZE
		self.tilepos = vec(int(self.pos.x / TILESIZE), int(self.pos.y / TILESIZE))
		self.chunkpos = vec(int(self.tilepos.x / CHUNKSIZE), int(self.tilepos.y / CHUNKSIZE))
		self.chunkrect = pg.Rect(self.rect.x, self.rect.y, CHUNKTILESIZE, CHUNKTILESIZE)
		n = random.randint(0, 3)
		if n == 0:
			self.image = pg.transform.flip(self.image, true, true)
		if n == 1:
			self.image = pg.transform.flip(self.image, false, true)
		if n == 2:
			self.image = pg.transform.flip(self.image, true, false)
