import pygame as pg
from settings import *
from textures import *
import pygame as pg

# HUD ───────────────────────────────────



class Hotbar(pg.sprite.Sprite):

	def __init__(self, game):
		self._layer = 1
		self.groups = game.gui
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = UI["HUD"]["hotbar"]
		self.rect = self.image.get_rect()
		self.player = self.game.player
		self.hand = "hand"
		self.rect.centerx = WIDTH / 2 + self.player.rect.width / 2
		self.rect.y = HEIGHT - self.rect.height - UI_MARGIN

		self.hblabel1 = (self.rect.x + self.rect.width / 3 - UI_MARGIN - 10, self.rect.centery + self.rect.height / 7)
		self.hblabel2 = (self.rect.x + (self.rect.width / 3) * 2 - UI_MARGIN - 13, self.rect.centery + self.rect.height / 7)
		self.hblabel3 = (self.rect.x + self.rect.width - UI_MARGIN - 16, self.rect.centery + self.rect.height / 7)

	def update(self):

		# Spawn placeholder on the hotbar
		if self.player.fullinv[0]["item"] and not self.player.hotbar_display[0]:
			self.player.hotbar_display[0] = ItemPlaceholder(self.game, "hb1", self.player.fullinv[0]["item"])
		if self.player.fullinv[1]["item"] and not self.player.hotbar_display[1]:
			self.player.hotbar_display[1] = ItemPlaceholder(self.game, "hb2", self.player.fullinv[1]["item"])
		if self.player.fullinv[2]["item"] and not self.player.hotbar_display[2]:
			self.player.hotbar_display[2] = ItemPlaceholder(self.game, "hb3", self.player.fullinv[2]["item"])

		# Spawn placeholder on hand
		if not self.player.holding:
			self.player.holding = ItemPlaceholder(self.game, self.hand, null)

		# Show item on hand
		if self.player.selected_slot != -1 and self.player.hotbar[self.player.selected_slot]["count"] > 0:

			if self.game.player.vel.x > 0:
				self.player.holding.image = pg.transform.flip(ITEMS[self.player.hotbar[self.player.selected_slot]["item"]], true, false)
			if self.game.player.vel.x < 0:
				self.player.holding.image = ITEMS[self.player.hotbar[self.player.selected_slot]["item"]]
			else:
				self.player.holding.image = ITEMS[self.player.hotbar[self.player.selected_slot]["item"]]

		# Remove the hand placeholder
		elif self.player.selected_slot != -1 and not self.player.hotbar[self.player.selected_slot]["item"]:
			self.player.holding.image = pg.Surface((1,1))
		elif self.player.holding and self.player.selected_slot == -1:
			self.player.holding.image = pg.Surface((1,1))

class HotbarPointer(pg.sprite.Sprite):
	def __init__(self, game):
		self._layer = 2
		self.groups = game.gui
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = UI["HUD"]["hb_pointer"]
		self.rect = self.image.get_rect()
		self.offset = 0

	def update(self):
		self.get_keys()
		self.rect.centerx = self.game.hotbar.rect.centerx + self.offset
		self.rect.y = self.game.hotbar.rect.y -self.rect.height - UI_MARGIN

	def get_keys(self):

		if self.game.player.selected_slot == 0:
			self.offset = -self.game.hotbar.rect.width / 3
			self.image = UI["HUD"]["hb_pointer"]
		elif self.game.player.selected_slot == 1:
			self.offset = 0
			self.image = UI["HUD"]["hb_pointer"]
		elif self.game.player.selected_slot == 2:
			self.offset = self.game.hotbar.rect.width / 3
			self.image = UI["HUD"]["hb_pointer"]
		else:
			self.image = pg.Surface((1, 1))

class ItemPlaceholder(pg.sprite.Sprite):
	def __init__(self, game, slot, item):
		self._layer = 3
		self.groups = game.placeholders, game.gui
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.item = item
		if item in ITEMS:
			self.oimage = ITEMS[item]
		else:
			self.oimage = pg.Surface((1,1))
		self.image = self.oimage
		self.orect = self.image.get_rect()
		self.rect = self.orect.copy()
		self.hotbar = self.game.hotbar.rect
		self.inv_hotbar = self.game.inventory.hotbar_rect
		self.inventory = self.game.inventory.rect
		self.player = self.game.player
		self.slot = slot
		self.handoffset = vec(-30, 0)
		self.visible = true

		self.hand = WIDTH / 2 + self.game.player.rect.width / 2 + self.handoffset.x, HEIGHT / 2 + self.game.player.rect.height / 2 + self.handoffset.y

		self.hb1 = (self.hotbar.centerx - self.hotbar.width / 3 + 3, self.hotbar.centery)
		self.hb2 = self.hotbar.center
		self.hb3 = (self.hotbar.centerx + self.hotbar.width / 3 - 3, self.hotbar.centery)

		self.slots = {
		0: (self.inventory.centerx - self.inventory.width / 3 + 6, self.inv_hotbar.centery),
		1: (self.inventory.centerx, self.inv_hotbar.centery),
		2: (self.inventory.centerx + self.inventory.width / 3 - 6, self.inv_hotbar.centery),
		3: (self.inventory.centerx - self.inventory.width / 3 + 6, self.inventory.centery - self.inventory.height / 4 + 6),
		4: (self.inventory.centerx, self.inventory.centery - self.inventory.height / 4 + 6),
		5: (self.inventory.centerx + self.inventory.width / 3 - 6, self.inventory.centery - self.inventory.height / 4 + 6),
		6: (self.inventory.centerx - self.inventory.width / 3 + 6, self.inventory.centery + self.inventory.height / 4 - 6),
		7: (self.inventory.centerx, self.inventory.centery + self.inventory.height / 4 - 6),
		8: (self.inventory.centerx + self.inventory.width / 3 - 6, self.inventory.centery + self.inventory.height / 4 - 6)
		}

	def update(self):
		if self.game.player.vel.x > 0:
			self.handoffset = vec(-30, 0)
		if self.game.player.vel.x < 0:
			self.handoffset = vec(-5, 0)

		if self.slot == "hand":
			self.rect.center = self.hand
		if self.slot == "hb1":
			self.rect.center = self.hb1
		if self.slot == "hb2":
			self.rect.center = self.hb2
		if self.slot == "hb3":
			self.rect.center = self.hb3

		if self.slot in self.slots:
			self.visible = self.game.inventory.visible
			self.image = pg.transform.scale(self.oimage, (self.orect.width * 2, self.orect.height * 2))
			self.rect = self.image.get_rect()
			self.rect.center = self.slots[self.slot]


# UI ───────────────────────────────────────

class Inventory(pg.sprite.Sprite):

	def __init__(self, game):
		self.game = game
		self.groups = game.gui
		pg.sprite.Sprite.__init__(self, self.groups)
		self.visible = false
		self.image = UI['pinv']
		self.rect = self.image.get_rect()
		self.offset = self.rect.height / 3
		self.rect.center = vec(WIDTH / 2 + self.game.player.rect.width / 2, HEIGHT / 2 - self.offset)
		self.player = game.player

		self.font = pg.font.Font("textures/fonts/ttp.otf", 15)

		self.hotbar_img = pg.transform.scale(self.game.hotbar.image.copy(), (self.game.hotbar.rect.width * 2, self.game.hotbar.rect.height * 2))
		self.hotbar_rect = self.hotbar_img.get_rect()
		self.hotbar_rect.center = vec(WIDTH / 2 + self.game.player.rect.width / 2, HEIGHT / 2 + self.offset * 1.5)

		self.label_offset = vec(20, 25)

		self.labelpos = {
		0: (self.rect.centerx - self.rect.width / 3 + 6, self.hotbar_rect.centery) + self.label_offset,
		1: (self.rect.centerx, self.hotbar_rect.centery) + self.label_offset,
		2: (self.rect.centerx + self.rect.width / 3 - 6, self.hotbar_rect.centery) + self.label_offset,

		3: (self.rect.centerx - self.rect.width / 3 + 6, self.rect.centery - self.rect.height / 4 + 6) + self.label_offset,
		4: (self.rect.centerx, self.rect.centery - self.rect.height / 4 + 6) + self.label_offset,
		5: (self.rect.centerx + self.rect.width / 3 - 6, self.rect.centery - self.rect.height / 4 + 6) + self.label_offset,

		6: (self.rect.centerx - self.rect.width / 3 + 6, self.rect.centery + self.rect.height / 4 - 6) + self.label_offset,
		7: (self.rect.centerx, self.rect.centery + self.rect.height / 4 - 6) + self.label_offset,
		8: (self.rect.centerx + self.rect.width / 3 - 6, self.rect.centery + self.rect.height / 4 - 6) + self.label_offset
		}


	def update(self):
		if self.player.on_inv:
			self.visible = true
		else:
			self.visible = false

		if self.player.fullinv[0]["item"] and not self.player.inv_display[0]:
			self.player.inv_display[0] = ItemPlaceholder(self.game, 0, self.player.fullinv[0]["item"])

		if self.player.fullinv[1]["item"] and not self.player.inv_display[1]:
			self.player.inv_display[1] = ItemPlaceholder(self.game, 1, self.player.fullinv[1]["item"])

		if self.player.fullinv[2]["item"] and not self.player.inv_display[2]:
			self.player.inv_display[2] = ItemPlaceholder(self.game, 2, self.player.fullinv[2]["item"])

		if self.player.fullinv[3]["item"] and not self.player.inv_display[3]:
			self.player.inv_display[3] = ItemPlaceholder(self.game, 3, self.player.fullinv[3]["item"])

		if self.player.fullinv[4]["item"] and not self.player.inv_display[4]:
			self.player.inv_display[4] = ItemPlaceholder(self.game, 4, self.player.fullinv[4]["item"])

		if self.player.fullinv[5]["item"] and not self.player.inv_display[5]:
			self.player.inv_display[5] = ItemPlaceholder(self.game, 5, self.player.fullinv[5]["item"])

		if self.player.fullinv[6]["item"] and not self.player.inv_display[6]:
			self.player.inv_display[6] = ItemPlaceholder(self.game, 6, self.player.fullinv[6]["item"])

		if self.player.fullinv[7]["item"] and not self.player.inv_display[7]:
			self.player.inv_display[7] = ItemPlaceholder(self.game, 7, self.player.fullinv[7]["item"])

		if self.player.fullinv[8]["item"] and not self.player.inv_display[8]:
			self.player.inv_display[8] = ItemPlaceholder(self.game, 8, self.player.fullinv[8]["item"])

		self.label = {
		0: self.font.render(str(self.player.fullinv[0]['count']), 1, WHITE),
		1: self.font.render(str(self.player.fullinv[1]['count']), 1, WHITE),
		2: self.font.render(str(self.player.fullinv[2]['count']), 1, WHITE),

		3: self.font.render(str(self.player.fullinv[3]['count']), 1, WHITE),
		4: self.font.render(str(self.player.fullinv[4]['count']), 1, WHITE),
		5: self.font.render(str(self.player.fullinv[5]['count']), 1, WHITE),

		6: self.font.render(str(self.player.fullinv[6]['count']), 1, WHITE),
		7: self.font.render(str(self.player.fullinv[7]['count']), 1, WHITE),
		8: self.font.render(str(self.player.fullinv[8]['count']), 1, WHITE)
		}

		if self.visible:
			for i in self.label:
				if self.player.fullinv[i]['count'] > 1:
					self.game.screen.blit(self.label[i], self.labelpos[i])


# Menu ─────────────────────────────────────

class Menu(pg.sprite.Sprite):

	def __init__(self):
		pass
