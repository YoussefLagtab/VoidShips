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
		self.rect.centerx = WIDTH / 2 + self.player.rect.width / 2
		self.rect.y = HEIGHT - self.rect.height - UI_MARGIN

		self.hblabel1 = (self.rect.x + self.rect.width / 3 - UI_MARGIN - 5, self.rect.centery + self.rect.height / 7)
		self.hblabel2 = self.rect.x + (self.rect.width / 3) * 2 - UI_MARGIN - 8, self.rect.centery + self.rect.height / 7
		self.hblabel3 = (self.rect.x + self.rect.width - UI_MARGIN - 11, self.rect.centery + self.rect.height / 7)

	def update(self):


		if self.player.hotbar[0]['item'] and not self.player.hotbar_display[0]:
			self.player.hotbar_display[0] = ItemPlaceholder(self.game, self.slot1, self.player.hotbar[0]['item'])
		if self.player.hotbar[1]['item'] and not self.player.hotbar_display[1]:
			self.player.hotbar_display[1] = ItemPlaceholder(self.game, self.slot2, self.player.hotbar[1]['item'])
		if self.player.hotbar[2]['item'] and not self.player.hotbar_display[2]:
			self.player.hotbar_display[2] = ItemPlaceholder(self.game, self.slot3, self.player.hotbar[2]['item'])

		if not self.player.holding:
			self.player.holding = ItemPlaceholder(self.game, self.hand, null)

		if self.player.selected_slot != -1 and self.player.hotbar[self.player.selected_slot]['count'] > 0:

			if self.game.player.vel.x > 0:
				self.player.holding.image = pg.transform.flip(ITEMS[self.player.hotbar[self.player.selected_slot]['item']], true, false)
			if self.game.player.vel.x < 0:
				self.player.holding.image = ITEMS[self.player.hotbar[self.player.selected_slot]['item']]
			else:
				self.player.holding.image = ITEMS[self.player.hotbar[self.player.selected_slot]['item']]

		elif self.player.selected_slot != -1 and not self.player.hotbar[self.player.selected_slot]['item']:
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
		self.rect.centerx = self.game.hotbar.rect.centerx + self.offset
		self.rect.y = self.game.hotbar.rect.y -self.rect.height - UI_MARGIN

	def get_keys(self):

		if self.game.player.selected_slot == 0:
			self.offset = -self.game.hotbar.rect.width / 3
			self.image = UI['HUD']['hb_pointer']
		elif self.game.player.selected_slot == 1:
			self.offset = 0
			self.image = UI['HUD']['hb_pointer']
		elif self.game.player.selected_slot == 2:
			self.offset = self.game.hotbar.rect.width / 3
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
		self.handoffset = vec(-5, 0)

	def update(self):
		if self.game.player.vel.x > 0:
			self.handoffset = vec(-30, 0)
		if self.game.player.vel.x < 0:
			self.handoffset = vec(-5, 0)


		self.hold = WIDTH / 2 + self.game.player.rect.width / 2 + self.handoffset.x, HEIGHT / 2 + self.game.player.rect.height / 2 + self.handoffset.y


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
