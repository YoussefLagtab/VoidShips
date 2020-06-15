#!/usr/bin/python3.7
import pygame as pg
from scripts import *
from objects import *
from textures import *
from chunk_manager import *

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

		self.ui.update()

	# Load the blocks and items from the chunk given by the ChunkManager loader
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
				if tile == '.':
					Void(self, x, y)
				if tile == '#':
					Block(self, x, y, 'grass')
				if tile == '@':
					Block(self, x, y, 'mountain')

			for i in items:
				item = i[0]
				x = i[1]
				y = i[2]
				if item == "A":
					Item(self, x, y, "heart")
				if item == 'i':
					Item(self, x, y, "stone")

	# Save the game
	def save(self):
		chunkmanager.save()

	# Update the map
	def reload_chunks(self):
		# Define render area
		for cname in self.area:
			chunk = tuple(cname.split(','))
			cx = int(chunk[0])
			cy = int(chunk[1])
			if cname not in chunkmanager.get_chunks():
				chunkmanager.generate(cx, cy)
			self.load_chunk(chunkmanager.load(cx, cy))

		for cname in chunkmanager.get_chunks():
			chunk = cname.split(',')
			chunk = (int(chunk[0]), int(chunk[1]))
			if cname not in self.area and cname in chunkmanager.get_loaded():
				for sprite in self.all_sprites:
					if sprite != self.player and sprite.chunkpos == chunk:
						sprite.kill()
				chunkmanager.unload(cname)

		for item in self.items:
			for void in self.void:
				if item.pos == void.pos:
					item.kill()

	def hit_items(self):
		hits = pg.sprite.spritecollide(self.player, self.items, false)
		if hits:
			for slot in self.player.hotbar:
				if self.player.hotbar[slot] == null:
					self.player.hotbar[slot] = hits[0].item
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
		for y in range(-CHUNKRENDERY, CHUNKRENDERY + 1):
			for x in range(-CHUNKRENDERX, CHUNKRENDERX + 1):
				cx = int(px + x)
				cy = int(py + y)
				cname = str(cx) + ',' + str(cy)
				self.area.append(cname)

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
		#Make sure that not loaded parts of the map don't get the windows XP window duplicating effect
		self.screen.fill(BLACK)

		#Show all sprites on screen
		for sprite in self.all_sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
			if self.draw_debug:
				if sprite != self.player and sprite not in self.void:
					pg.draw.rect(self.screen, LIGHTGREY, self.camera.apply_rect(sprite.rect), 2)


				# Draw the player's hitbox (white) and it's position (red)
				pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(self.player.hit_rect), 2)
				pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(self.player.rect), 2)
				pg.draw.rect(self.screen, RED, self.camera.apply_rect(pg.Rect(*self.player.pos, 4, 4)))

		for object in self.ui:
			self.screen.blit(object.image, self.camera.apply(object))

	#Recieve some input for basic general control
	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sys.exit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					chunkmanager.save()
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
