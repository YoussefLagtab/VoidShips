#!/usr/bin/python3.7
import pickle

import pygame as pg
from objects import *
from scripts import *
from textures import *

index = 0

class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(SIZE)
		self.state = 0
		self.create()
	# Create groups and global variables
	def create(self):

		self.clock = pg.time.Clock()


		# Define sprite groups ─────────────────────────────
		self.all_sprites = pg.sprite.LayeredUpdates()
		self.blocks = pg.sprite.Group()
		self.walls = pg.sprite.Group()
		self.collidables = pg.sprite.Group()
		self.entities = pg.sprite.Group()
		self.items = pg.sprite.Group()
		self.animals = pg.sprite.Group()
		self.enemies = pg.sprite.Group()
		self.void = pg.sprite.Group()
		self.floortiles = pg.sprite.Group()
		self.grass = pg.sprite.Group()
		self.gui = pg.sprite.LayeredUpdates()
		self.placeholders = pg.sprite.Group()
		# ──────────────────────────────────────────────────

		self.player = null
		if self.player == null:
			self.player = Player(self, *PLAYER_DEFAULT_SPAWN)
		self.timecounter = 0
		self.camera = Camera(0, 0)
		self.draw_debug = false
		self.area = []
		self.old_area = []


		# UI ELEMENTS ̣──────────────────────────────────────
		self.hotbar = Hotbar(self)
		self.hb_pointer = HotbarPointer(self)
		self.inventory = Inventory(self)
		# ──────────────────────────────────────────────────

		# Fonts ────────────────────────
		self.hotbarFont = pg.font.Font("textures/fonts/ttp.otf", 10)
		# ──────────────────────────────

		self.entry = Entry(self, 10, 10, 1000, 20, self.enter_world, "textures/fonts/ttp.otf")
		self.entry.typing = true

		self.mouseItem = null
		self.mouseCount = 0
		self.mouseDummy = ItemPlaceholder(self, 9, null)
	# Change the state to in_game and create the world
	def enter_world(self):
		self.state = 1
		self.name = str(self.entry.text)
		self.create_world()
	# Create the world
	def create_world(self):

		try:
			print('Entering world "{}"'.format(self.name))
			with open("worlds/"+self.name+".data", 'rb') as f:
				self.world_data = pickle.load(f)
				print(self.world_data['seed'])
			self.worldmanager = WorldManager(self.world_data['map'], self.world_data['seed'], self.world_data["world_name"])

		except:
			print('World "{}" not found. Generating a new one...'.format(self.name))
			with open("worlds/"+self.name+".data", 'wb') as f:
				pickle.dump(DEFAULT_WORLD_FORMAT, f)
			with open("worlds/"+self.name+".data", 'rb') as f:
				self.world_data = pickle.load(f)
				print(self.world_data)

			try:
				self.worldmanager = WorldManager(DEFAULT_WORLD_FORMAT['map'], seedgen, self.name)
			except:
				pass

		self.player.load_data(self.world_data["player"])
	# Load the blocks and items from the chunk given by the worldmanager loader
	def load_chunk(self, data):
		if data != null:
			#parse the data
			tile = str()
			x = int()
			y = int()
			floor = data[0]
			items = data[1]
			for i in floor:
				tile = i[0]
				x = i[1]
				y = i[2]
				if tile == ".":
					Void(self, x, y)
				if tile == "#":
					Block(self, x, y, "grass")
				if tile == "@":
					Block(self, x, y, "mountain")

			for i in items:
				item = i[0]
				x = i[1]
				y = i[2]
				if item == "A":
					Item(self, x, y, "heart")
				if item == "i":
					Item(self, x, y, "stone")
	# Save the game
	def save(self):
		self.world_data.update({"world_name" : self.worldmanager.get_name(), "seed" : self.worldmanager.get_seed(), "map" : self.worldmanager.save(), "player" : self.player.save_data()})
		with open("worlds/"+self.worldmanager.get_name() +".data", "wb") as f:
			pickle.dump(self.world_data, f)
	# Update the map
	def reload_chunks(self):
		# Define render area
		for chunk in self.area:
			if chunk not in self.worldmanager.get_chunks():
				self.worldmanager.generate(chunk[0], chunk[1])
			self.load_chunk(self.worldmanager.load(chunk[0], chunk[1]))

		for chunk in self.worldmanager.get_chunks():
			if chunk not in self.area and chunk in self.worldmanager.get_loaded():
				for sprite in self.all_sprites:
					if sprite != self.player and sprite.chunkpos == chunk:
						sprite.kill()
				self.worldmanager.unload(chunk)

		for item in self.items:
			for void in self.void:
				if item.pos == void.pos:
					item.kill()
	# Detect collision with items
	def hit_items(self):
		hits = pg.sprite.spritecollide(self.player, self.items, false)
		if hits:
			for hit, item in enumerate(hits):
				# Iterate through each slot in the inventory of the player
				for slot in self.player.fullinv:
					# If it finds an empty slot, put the item in there
					if self.player.fullinv[slot]["item"] == "empty":
						self.player.fullinv[slot]["item"] = hits[hit].item
						# self.player.fullinv[slot]["count"] += 1
						self.worldmanager.kill_item(hits[hit].chunkpos, hits[hit].tilepos)
						hits[hit].kill()
						break
					# If it finds a slot with the same item that has been hit, if the count is less than MAXITEMS, add it to the slot
					elif self.player.fullinv[slot]["item"] == hits[hit].item and self.player.fullinv[slot]["count"] < MAXITEMS:
						self.player.fullinv[slot]["count"] += 1
						self.worldmanager.kill_item(hits[hit].chunkpos, hits[hit].tilepos)
						hits[hit].kill()
						break
	# Call each function in the correct order for the game to run properly
	def run(self):
		if self.state == GAME_STATES['ingame']:
			self.delta = self.clock.tick(FPS) / 1000.0
			self.events()
			self.draw()
			self.update()

			# Save the game every once in a while
			if self.timecounter < savetimer:
				self.timecounter += 1
			else:
				self.timecounter = 0
				self.save()
		elif self.state == GAME_STATES['onmenu']:
			self.entry.update()
			pg.display.update()
		elif self.state == GAME_STATES['paused']:
			pass
		elif self.state == GAME_STATES['gameover']:
			pass
	# Update all sprites and update the render area
	def update(self):

		# Call update() on all sprites
		self.all_sprites.update()
		self.gui.update()

		# Update the mouse dummy
		self.mouseDummy.item = self.mouseItem
		self.mouseDummy.count = self.mouseCount

		# Show FPS for debbugging purposes
		pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

		# Move the camera to the player
		self.camera.update(self.player)

		# Define a render area around the player
		px = int(self.player.chunkpos.x)
		py = int(self.player.chunkpos.y)
		self.area = []
		for y in range(-CHUNKRENDER, CHUNKRENDER + 1):
			for x in range(-CHUNKRENDER, CHUNKRENDER + 1):
				cx = int(px + x)
				cy = int(py + y)
				chunkname = (cx, cy)
				self.area.append(chunkname)

		# Call the chunks to reload when the area changes
		if self.area != self.old_area:
			self.old_area = self.area
			self.reload_chunks()

		self.hit_items()

		# Update the screen
		pg.display.update()
	# Draw a grid for debugging purposes
	def grid(self):
		for x in range(TILEWIDTH):
			pg.draw.line(self.screen, LIGHTGREY, (x*TILESIZE, 0), (x*TILESIZE, HEIGHT))
		for y in range(TILEHEIGHT):
			pg.draw.line(self.screen, LIGHTGREY, (0, y*TILESIZE), (WIDTH, y*TILESIZE))
	# Display player's inventory contents on screen
	def show_inv_content(self):
		l0 = self.hotbarFont.render("0 : Item: " + str(self.player.fullinv[0]["item"]) + " - Count: " + str(self.player.fullinv[0]["count"]), 1, WHITE)
		l1 = self.hotbarFont.render("1 : Item: " + str(self.player.fullinv[1]["item"]) + " - Count: " + str(self.player.fullinv[1]["count"]), 1, WHITE)
		l2 = self.hotbarFont.render("2 : Item: " + str(self.player.fullinv[2]["item"]) + " - Count: " + str(self.player.fullinv[2]["count"]), 1, WHITE)
		l3 = self.hotbarFont.render("3 : Item: " + str(self.player.fullinv[3]["item"]) + " - Count: " + str(self.player.fullinv[3]["count"]), 1, WHITE)
		l4 = self.hotbarFont.render("4 : Item: " + str(self.player.fullinv[4]["item"]) + " - Count: " + str(self.player.fullinv[4]["count"]), 1, WHITE)
		l5 = self.hotbarFont.render("5 : Item: " + str(self.player.fullinv[5]["item"]) + " - Count: " + str(self.player.fullinv[5]["count"]), 1, WHITE)
		l6 = self.hotbarFont.render("6 : Item: " + str(self.player.fullinv[6]["item"]) + " - Count: " + str(self.player.fullinv[6]["count"]), 1, WHITE)
		l7 = self.hotbarFont.render("7 : Item: " + str(self.player.fullinv[7]["item"]) + " - Count: " + str(self.player.fullinv[7]["count"]), 1, WHITE)
		l8 = self.hotbarFont.render("8 : Item: " + str(self.player.fullinv[8]["item"]) + " - Count: " + str(self.player.fullinv[8]["count"]), 1, WHITE)
		mouse = self.hotbarFont.render("Mouse : Item: " + str(self.mouseItem) + " - Count: " + str(self.mouseCount), 1, WHITE)

		self.screen.blit(l0, (10, 10))
		self.screen.blit(l1, (10, 30))
		self.screen.blit(l2, (10, 50))
		self.screen.blit(l3, (10, 70))
		self.screen.blit(l4, (10, 90))
		self.screen.blit(l5, (10, 110))
		self.screen.blit(l6, (10, 130))
		self.screen.blit(l7, (10, 150))
		self.screen.blit(l8, (10, 170))
		self.screen.blit(mouse, (10, 200))

		if self.draw_debug:
			if self.inventory.visible:
				for rect in self.inventory.empty_slots:
					pg.draw.rect(self.screen, WHITE, self.inventory.empty_slots[rect], 3)

				for ph in self.placeholders:
					pg.draw.rect(self.screen, WHITE, ph.rect, 3)
	# Draw the sprites
	def draw(self):
		#Make sure that not loaded parts of the map don"t get the windows XP window duplicating effect
		self.screen.fill(BLACK)

		#Show all sprites on screen
		for sprite in self.all_sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
			if self.draw_debug:
				if sprite != self.player and sprite not in self.void:
					pg.draw.rect(self.screen, LIGHTGREY, self.camera.apply_rect(sprite.rect), 2)


				# Draw the player"s hitbox (white) and it"s position (red)
				pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(self.player.hit_rect), 2)
				pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(self.player.rect), 2)
				pg.draw.rect(self.screen, RED, self.camera.apply_rect(pg.Rect(*self.player.pos, 4, 4)))


		self.screen.blit(self.hotbar.image, self.hotbar.rect.topleft)
		self.screen.blit(self.hb_pointer.image, self.hb_pointer.rect.topleft)
		if self.inventory.visible:
			self.screen.blit(self.inventory.image, self.inventory.rect.topleft)
			self.screen.blit(self.inventory.hotbar_img, self.inventory.hotbar_rect.topleft)

		for ph in self.placeholders:
			if ph.visible and ph.image:
				self.screen.blit(ph.image, ph.rect.topleft)

		hotbarlabel1 = self.hotbarFont.render(str(self.player.fullinv[0]["count"]), 1, WHITE)
		hotbarlabel2 = self.hotbarFont.render(str(self.player.fullinv[1]["count"]), 1, WHITE)
		hotbarlabel3 = self.hotbarFont.render(str(self.player.fullinv[2]["count"]), 1, WHITE)

		if self.player.fullinv[0]["count"] > 1:
			self.screen.blit(hotbarlabel1, self.hotbar.hblabel1)
		if self.player.fullinv[1]["count"] > 1:
			self.screen.blit(hotbarlabel2, self.hotbar.hblabel2)
		if self.player.fullinv[2]["count"] > 1:
			self.screen.blit(hotbarlabel3, self.hotbar.hblabel3)

		#self.show_inv_content()
	#Recieve some input for basic general control
	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sys.exit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					if self.player.on_inv:
						self.player.on_inv = false
					else:
						self.save()
						sys.exit()
				if event.key == pg.K_h:
					self.draw_debug = not self.draw_debug

				if event.key == pg.K_1:
					if self.player.selected_slot == 0:
						self.player.selected_slot = -1
					else:
						self.player.selected_slot = 0

				if event.key == pg.K_2:
					if self.player.selected_slot == 1:
						self.player.selected_slot = -1
					else:
						self.player.selected_slot = 1

				if event.key == pg.K_3:
					if self.player.selected_slot == 2:
						self.player.selected_slot = -1
					else:
						self.player.selected_slot = 2

				if event.key == pg.K_e and not self.mouseItem:
					self.player.on_inv = not self.player.on_inv

				if event.key == pg.K_p:
					self.player.fullinv = DEFAULT_WORLD_FORMAT['player']['fullinv']

#Main loop
g = Game()
while true:
	g.run()
