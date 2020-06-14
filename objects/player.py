import pygame as pg
from settings import *
from textures import *

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = PLAYER_LAYER
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = PLAYER_IMG
		self.rect = self.image.get_rect()
		self.vel = vec(0,0)
		self.pos = vec(x, y) * TILESIZE
		self.tilepos = vec(int(self.pos.x / TILESIZE), int(self.pos.y / TILESIZE))
		self.chunkpos = self.tilepos * CHUNKSIZE
		self.name = "Chris"

	# Get input for player movement
	def get_keys(self):
		self.vel = vec(0,0)
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.vel.x = -PLAYER_SPEED
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.vel.x = PLAYER_SPEED
		if keys[pg.K_UP] or keys[pg.K_w]:
			self.vel.y = -PLAYER_SPEED
		if keys[pg.K_DOWN] or keys[pg.K_s]:
			self.vel.y = PLAYER_SPEED
		if self.vel.x != 0 and self.vel.y != 0:
			self.vel *= 0.7071

	# Make the player collide with the walls
	def collide_with_walls(self, dir):
		if dir == 'x':
			hits = pg.sprite.spritecollide(self, self.game.collidables, False)
			if hits:
				if self.vel.x > 0:
					self.pos.x = hits[0].rect.left - self.rect.width
				if self.vel.x < 0:
					self.pos.x = hits[0].rect.right
				self.vel.x = 0
				self.rect.x = self.pos.x
		if dir == 'y':
			hits = pg.sprite.spritecollide(self, self.game.collidables, False)
			if hits:
				if self.vel.y > 0:
					self.pos.y = hits[0].rect.top - self.rect.height
				if self.vel.y < 0:
					self.pos.y = hits[0].rect.bottom
				self.vel.y = 0
				self.rect.y = self.pos.y

	# Update the player values
	def update(self):
		self.get_keys()
		self.pos += self.vel * self.game.delta
		self.rect.x = self.pos.x
		# self.collide_with_walls('x')
		self.rect.y = self.pos.y
		# self.collide_with_walls('y')
		self.tilepos = vec(int(self.pos.x / TILESIZE), int(self.pos.y / TILESIZE))
		self.chunkpos = vec(int(self.tilepos.x / CHUNKSIZE), int(self.tilepos.y / CHUNKSIZE))
		if self.pos.x < XLIMIT:
			print("You have reached the edge of the world!")
			self.pos.x = XLIMIT
		if self.pos.y < YLIMIT:
			print("You have reached the edge of the world!")
			self.pos.y = YLIMIT
