import pygame as pg
from settings import *
from textures import *

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
			self.player.holding = ItemPlaceholder(self.game, self.hand, "empty")

		# Show item on hand
		if self.player.selected_slot != -1 and self.player.fullinv[self.player.selected_slot]["count"] > 0:

			if self.game.player.vel.x > 0:
				self.player.holding.image = pg.transform.flip(ITEMS[self.player.fullinv[self.player.selected_slot]["item"]], true, false)
			if self.game.player.vel.x < 0:
				self.player.holding.image = ITEMS[self.player.fullinv[self.player.selected_slot]["item"]]
			else:
				self.player.holding.image = ITEMS[self.player.fullinv[self.player.selected_slot]["item"]]

		# Remove the hand placeholder
		elif self.player.selected_slot != -1 and not self.player.fullinv[self.player.selected_slot]["item"]:
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
		self.count = 1
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
		self.inv = self.game.inventory
		self.player = self.game.player
		self.slot = slot
		self.handoffset = vec(-30, 0)
		self.visible = true
		self.hasMoved = 99
		self.on_mouse = false

		self.hand = WIDTH / 2 + self.game.player.rect.width / 2 + self.handoffset.x, HEIGHT / 2 + self.game.player.rect.height / 2 + self.handoffset.y

		self.hb1 = (self.hotbar.centerx - self.hotbar.width / 3 + 3, self.hotbar.centery)
		self.hb2 = self.hotbar.center
		self.hb3 = (self.hotbar.centerx + self.hotbar.width / 3 - 3, self.hotbar.centery)

		self.slots = {
		0: self.inv.empty_slots[0].center,
		1: self.inv.empty_slots[1].center,
		2: self.inv.empty_slots[2].center,
		3: self.inv.empty_slots[3].center,
		4: self.inv.empty_slots[4].center,
		5: self.inv.empty_slots[5].center,
		6: self.inv.empty_slots[6].center,
		7: self.inv.empty_slots[7].center,
		8: self.inv.empty_slots[8].center
		}

		self.hotbar_slots = {
		0:"hb1",
		1:"hb2",
		2:"hb3"}

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

		self.label_offset = vec(20, 25)
		self.font = pg.font.Font("textures/fonts/ttp.otf", 15)

	def update(self):

		# Get mouse presses (1 : left, 2 : middle, 3 : right)
		mousepos = pg.mouse.get_pos()
		pressed1, pressed2, pressed3 = pg.mouse.get_pressed()

		# Change the offset of the hand dummy for the player
		if self.game.player.vel.x > 0:
			self.handoffset = vec(-30, 0)
		if self.game.player.vel.x < 0:
			self.handoffset = vec(-5, 0)

		# Hide dummies if the inventory is not visible
		if self.slot in self.slots:
			self.visible = self.game.inventory.visible

		# Make each dummy have the same count as the slot they're in
		for slot in self.slots:
			if self.slot == slot:
				self.count = self.player.fullinv[slot]['count']

		# Label for the number of items
		self.label = self.font.render(str(self.count), 1, WHITE)

		# Show the number of items in each slot
		if self.visible and self.slot in self.slots:
			if self.count > -1 and self.player.fullinv[self.slot]["item"] != "empty":
				self.game.screen.blit(self.label, self.rect.center + self.label_offset)

		# Show the number of items on the mouse
		if self == self.game.mouseDummy and self.game.mouseItem:
			self.game.screen.blit(self.label, self.rect.center + self.label_offset)

		# Make the hotbar have the same image as the hotbar part of the inventory
		for slot in self.hotbar_slots:
			if self.slot == self.hotbar_slots[slot]:
				self.image = ITEMS[self.player.fullinv[slot]["item"]]

		# Make the items in the inventory look bigger
		for slot in self.slots:
			for ph in self.game.placeholders:
				if ph.slot == slot:
					ph.image = pg.transform.scale(ITEMS[self.player.fullinv[slot]["item"]], (self.rect.width * 2, self.rect.height * 2))

		# Move items around the player's inventory
		for slot in self.inv.empty_slots:
			if self.slot in self.slots and self.inv.empty_slots[slot].collidepoint(mousepos) and self.player.on_inv:

				# Pick up
				if self.slot == slot and pressed1 and not self.game.mouseItem and self.player.fullinv[self.slot]["item"] != "empty":
					self.game.mouseItem = self.player.fullinv[self.slot]["item"]
					self.game.mouseCount = self.player.fullinv[self.slot]["count"]
					self.player.fullinv[self.slot]["item"] = "empty"
					self.player.fullinv[self.slot]["count"] = 1

				# Drop
				if pressed3 and self.game.mouseItem and self.player.fullinv[slot]["item"] == "empty":
					self.player.fullinv[slot]["item"] = self.game.mouseItem
					self.player.fullinv[slot]["count"] = self.game.mouseCount
					self.item = self.game.mouseItem
					self.count = self.game.mouseCount
					self.game.mouseItem = null
					self.game.mouseCount = 0
					self.hasMoved = slot

				# Swap
				if pressed3 and self.game.mouseItem and self.player.fullinv[slot]["item"] != "empty" and self.player.fullinv[slot]["item"] != self.game.mouseItem and self.hasMoved != slot:
					swapItem = self.player.fullinv[slot]["item"]
					swapCount = self.player.fullinv[slot]["count"]
					self.player.fullinv[slot]["item"] = self.game.mouseItem
					self.player.fullinv[slot]["count"] = self.game.mouseCount
					self.item = self.game.mouseItem
					self.count = self.game.mouseCount
					self.game.mouseItem = swapItem
					self.game.mouseCount = swapCount
					self.hasMoved = slot

				# Add
				if pressed3 and self.game.mouseItem and self.player.fullinv[slot]["item"] == self.game.mouseItem:
					sum = self.player.fullinv[slot]["count"] + self.game.mouseCount
					if sum > MAXITEMS:
						self.player.fullinv[slot]["count"] = MAXITEMS
						self.game.mouseCount = sum - MAXITEMS
					else:
						self.player.fullinv[slot]["count"] = sum
						self.game.mouseItem = null
						self.game.mouseCount = 0

		# Make the mouse dummy have the image of the item it's holding
		if self.item in ITEMS:
			self.oimage = ITEMS[self.item]
		else:
			self.oimage = null
		if self == self.game.mouseDummy:
			img = pg.transform.scale(self.oimage, (64, 64)) if self.oimage else null
			self.image = img

		# Move the mouse dummy to the mouse position
		if self == self.game.mouseDummy:
			self.rect.center = mousepos

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

		# Specify the positions of each slot
		self.slots = {
		0:(self.rect.centerx - self.rect.width / 3 + 6, self.hotbar_rect.centery),
		1:(self.rect.centerx, self.hotbar_rect.centery),
		2:(self.rect.centerx + self.rect.width / 3 - 6, self.hotbar_rect.centery),
		3:(self.rect.centerx - self.rect.width / 3 + 6, self.rect.centery - self.rect.height / 4 + 6),
		4:(self.rect.centerx, self.rect.centery - self.rect.height / 4 + 6),
		5:(self.rect.centerx + self.rect.width / 3 - 6, self.rect.centery - self.rect.height / 4 + 6),
		6:(self.rect.centerx - self.rect.width / 3 + 6, self.rect.centery + self.rect.height / 4 - 6),
		7:(self.rect.centerx, self.rect.centery + self.rect.height / 4 - 6),
		8:(self.rect.centerx + self.rect.width / 3 - 6, self.rect.centery + self.rect.height / 4 - 6)
		}

		# Create a rect for each slot to detect clicks
		self.empty_slots = {
		0: pg.Rect((0,0,96,96)),
		1: pg.Rect((0,0,96,96)),
		2: pg.Rect((0,0,96,96)),
		3: pg.Rect((0,0,96,96)),
		4: pg.Rect((0,0,96,96)),
		5: pg.Rect((0,0,96,96)),
		6: pg.Rect((0,0,96,96)),
		7: pg.Rect((0,0,96,96)),
		8: pg.Rect((0,0,96,96)),
		}

		# Move each rect to its position in the inventory
		for i in self.empty_slots:
			self.empty_slots[i].center = self.slots[i]

	def update(self):
		if self.player.on_inv:
			self.visible = true
		else:
			self.visible = false

		# Create a dummy for each slot in the inventory, based on the slot's content (even if it is empty)
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




# Menu ─────────────────────────────────────

class Menu(pg.sprite.Sprite):

	def __init__(self):
		pass
