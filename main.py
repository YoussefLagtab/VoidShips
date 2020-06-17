#!/usr/bin/python3.7
import pygame as pg
from scripts import *
from objects import *
from textures import *
import pickle

class Game:

	def __init__(self):
		pg.init()
		self.playing = true
		self.create()

	# Create groups and global variables
	def create(self):

		self.clock = pg.time.Clock()
		self.screen = pg.display.set_mode(SIZE)

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
		self.ui = pg.sprite.LayeredUpdates()
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
		# ──────────────────────────────────────────────────

		# Fonts ────────────────────────
		self.hotbarFont = pg.font.Font("textures/fonts/ttp.otf", 10)
		# ──────────────────────────────



		name = input("Enter world name: ")
		try:
			with open("worlds/"+name+".data", 'rb') as f:
				self.world_data = pickle.load(f)
			self.worldmanager = WorldManager(self.world_data['map'], self.world_data['seed'], self.world_data["world_name"])

		except:
			with open("worlds/"+name+".data", 'wb') as f:
				self.world_data = DEFAULT_WORLD_FORMAT
				pickle.dump(self.world_data, f)

			self.worldmanager = WorldManager(self.world_data['map'], null, name)

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
			for slot in self.player.hotbar:
				if not self.player.hotbar[slot]["item"]:
					self.player.hotbar[slot]["item"] = hits[0].item
					self.player.hotbar[slot]["count"] += 1
					self.worldmanager.kill_item(hits[0].chunkpos, hits[0].tilepos)
					hits[0].kill()
					break
				elif self.player.hotbar[slot]["item"] == hits[0].item and self.player.hotbar[slot]["count"] < MAXITEMS:
					self.player.hotbar[slot]["count"] += 1
					self.worldmanager.kill_item(hits[0].chunkpos, hits[0].tilepos)
					hits[0].kill()
					break

	# Call each function in the correct order for the game to run properly
	def run(self):
		if self.playing:
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

	# Update all sprites and update the render area
	def update(self):

		# Call update() on all sprites
		self.all_sprites.update()
		self.ui.update()

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

		for ph in self.placeholders:
			self.screen.blit(ph.image, ph.rect.topleft)

		hotbarlabel1 = self.hotbarFont.render(str(self.player.hotbar[0]["count"]), 1, WHITE)
		hotbarlabel2 = self.hotbarFont.render(str(self.player.hotbar[1]["count"]), 1, WHITE)
		hotbarlabel3 = self.hotbarFont.render(str(self.player.hotbar[2]["count"]), 1, WHITE)

		if self.player.hotbar[0]["count"] > 1:
			self.screen.blit(hotbarlabel1, self.hotbar.hblabel1)
		if self.player.hotbar[1]["count"] > 1:
			self.screen.blit(hotbarlabel2, self.hotbar.hblabel2)
		if self.player.hotbar[2]["count"] > 1:
			self.screen.blit(hotbarlabel3, self.hotbar.hblabel3)

	#Recieve some input for basic general control
	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sys.exit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.save()
					sys.exit()
				if event.key == pg.K_h:
					self.draw_debug = not self.draw_debug

				if event.key == pg.K_1:
					self.ui.update()
					if self.player.selected_slot == 0:
						self.player.selected_slot = -1
					else:
						self.player.selected_slot = 0
				if event.key == pg.K_2:
					self.ui.update()
					if self.player.selected_slot == 1:
						self.player.selected_slot = -1
					else:
						self.player.selected_slot = 1
				if event.key == pg.K_3:
					self.ui.update()
					if self.player.selected_slot == 2:
						self.player.selected_slot = -1
					else:
						self.player.selected_slot = 2

#Main loop
g = Game()
while true:
	g.run()
