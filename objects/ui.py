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
		self.slot1 = "hotbar0"
		self.slot2 = "hotbar1"
		self.slot3 = "hotbar2"
		self.hand = "hand"

	def update(self):
		self.rect.center = self.game.player.pos + vec(0, HEIGHT / 2 - self.rect.height - UI_MARGIN)

		if self.player.hotbar[0] and not self.player.hotbar_display[0]:
			self.player.hotbar_display[0] = ItemPlaceholder(self.game, self.slot1, self.player.hotbar[0])
		if self.player.hotbar[1] and not self.player.hotbar_display[1]:
			self.player.hotbar_display[1] = ItemPlaceholder(self.game, self.slot2, self.player.hotbar[1])
		if self.player.hotbar[2] and not self.player.hotbar_display[2]:
			self.player.hotbar_display[2] = ItemPlaceholder(self.game, self.slot3, self.player.hotbar[2])

		if not self.player.holding:
			self.player.holding = ItemPlaceholder(self.game, self.hand, null)

		if self.player.selected_slot != -1 and self.player.hotbar[self.player.selected_slot]:
			if self.game.player.vel.x > 0:
				self.player.holding.image = pg.transform.flip(ITEMS[self.player.hotbar[self.player.selected_slot]], true, false)
			if self.game.player.vel.x < 0:
				self.player.holding.image = ITEMS[self.player.hotbar[self.player.selected_slot]]
		elif self.player.selected_slot != -1 and not self.player.hotbar[self.player.selected_slot]:
			self.player.holding.image = pg.Surface((1,1))
		elif self.player.holding and self.player.selected_slot == -1:
			self.player.holding.image = pg.Surface((1,1))


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
		self.groups = game.placeholders, game.ui
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.item = item
		if item in ITEMS:
			self.image = ITEMS[item]
		else:
			self.image = pg.Surface((1,1))
		self.rect = self.image.get_rect()
		self.hotbar = self.game.hotbar.rect
		self.slot = slot
		self.offset = vec(25, 0)

	def update(self):
		if self.game.player.vel.x > 0:
			self.offset = vec(-30, 0)
		if self.game.player.vel.x < 0:
			self.offset = vec(-5, 0)


		self.hold = self.game.player.pos + self.offset

		print(self.offset)

		self.hotbar1 = (self.hotbar.centerx - self.hotbar.width / 3 + 3, self.hotbar.centery)
		self.hotbar2 = self.hotbar.center
		self.hotbar3 = (self.hotbar.centerx + self.hotbar.width / 3 - 3, self.hotbar.centery)

		if self.slot == "hotbar0":
			self.rect.center = self.hotbar1
		if self.slot == "hotbar1":
			self.rect.center = self.hotbar2
		if self.slot == "hotbar2":
			self.rect.center = self.hotbar3
		if self.slot == "hand":
			self.rect.center = self.hold



# UI ───────────────────────────────────────

class Inventory(pg.sprite.Sprite):


	def __init__(self):
		pass


# Menu ─────────────────────────────────────

class Menu(pg.sprite.Sprite):

	def __init__(self):
		pass
