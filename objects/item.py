import pygame as pg
from textures import *
from settings import *

class Item(pg.sprite.Sprite):
	def __init__(self, game, x, y, item):
		self._layer = ITEM_LAYER
		self.groups = game.all_sprites, game.items
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = ITEMS[item]
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.pos = vec(x, y) * TILESIZE
		self.rect.centerx = self.pos.x + TILESIZE/2
		self.rect.centery = self.pos.y + TILESIZE/2
		self.chunkpos = vec(int(x / CHUNKSIZE), int(y / CHUNKSIZE))
