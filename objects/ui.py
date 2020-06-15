import pygame as pg
from settings import *
from textures import *

# HUD ───────────────────────────────────



class Hotbar(pg.sprite.Sprite):

	def __init__(self, game):
		self._layer = 1
		self.groups = game.ui
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = UI['HUD']['hotbar']
		self.rect = self.image.get_rect()
		self.player = self.game.player
		self.slot1 = 0
		self.slot2 = 1
		self.slot3 = 2

	def update(self):
		self.rect.center = self.game.player.pos + vec(0, HEIGHT / 2 - self.rect.height - UI_MARGIN)

		if self.player.hotbar[0] != null and self.player.hotbar_display[0] == null:
			self.player.hotbar_display[0] = ItemPlaceholder(self.game, self.slot1, self.player.hotbar[0])

		if self.player.hotbar[1] != null and self.player.hotbar_display[1] == null:
			self.player.hotbar_display[1] = ItemPlaceholder(self.game, self.slot2, self.player.hotbar[1])

		if self.player.hotbar[2] != null and self.player.hotbar_display[2] == null:
			self.player.hotbar_display[2] = ItemPlaceholder(self.game, self.slot3, self.player.hotbar[2])

class HotbarPointer(pg.sprite.Sprite):
	def __init__(self, game):
		self._layer = 2
		self.groups = game.ui
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = UI['HUD']['hb_pointer']
		self.rect = self.image.get_rect()
		self.offset = 0

	def update(self):
		self.get_keys()
		self.rect.center = self.game.player.pos + vec(self.offset, HEIGHT / 2 - self.game.hotbar.rect.height * 2 - UI_MARGIN / 2)

	def get_keys(self):

		if self.game.player.selected_slot == 0:
			self.offset = -self.game.hotbar.rect.width / 3 + 3
			self.image = UI['HUD']['hb_pointer']
		elif self.game.player.selected_slot == 1:
			self.offset = 0
			self.image = UI['HUD']['hb_pointer']
		elif self.game.player.selected_slot == 2:
			self.offset = self.game.hotbar.rect.width / 3 - 3
			self.image = UI['HUD']['hb_pointer']
		else:
			self.image = pg.Surface((1, 1))

class ItemPlaceholder(pg.sprite.Sprite):
	def __init__(self, game, slot, item):
		self._layer = 3
		self.groups = game.ui
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.item = item
		self.image = ITEMS[item]
		self.rect = self.image.get_rect()
		self.hotbar = self.game.hotbar.rect
		self.slot = slot
		self.slot1 = (-self.hotbar.width / 3 + 3, self.rect.centery)
		self.slot2 = self.hotbar.center
		self.slot3 = (self.hotbar.width / 3 - 3, self.rect.centery)

	def update(self):
		self.slot1 = (self.hotbar.centerx - self.hotbar.width / 3 + 3, self.hotbar.centery)
		self.slot2 = self.hotbar.center
		self.slot3 = (self.hotbar.centerx + self.hotbar.width / 3 - 3, self.hotbar.centery)


		if self.slot == 0:
			self.rect.center = self.slot1
		if self.slot == 1:
			self.rect.center = self.slot2
		if self.slot == 2:
			self.rect.center = self.slot3



# UI ───────────────────────────────────────

class Inventory(pg.sprite.Sprite):


	def __init__(self):
		pass


# Menu ─────────────────────────────────────

class Menu(pg.sprite.Sprite):

	def __init__(self):
		pass
