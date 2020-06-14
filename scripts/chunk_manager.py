import noise
from settings import *
from objects import *
import json

class Chunk():

	def __init__(self):
		try:
			f = open("map.json", 'r+')
		except:
			f = open("map.json", 'w+')
			f.close()
			f = open("map.json", 'r+')
		file = f.read()
		self.chunks = {}
		if file != "":
			self.chunks = eval(file)
		f.close()
		self.loaded = []
		self.chunkname = str()
		self.unsaved = int()

	def get_chunks(self):
		return self.chunks

	def get_loaded(self):
		return self.loaded

	# remove given chunk from the loaded list, so it does not affect the performance
	def unload(self, chunk):
		self.loaded.remove(chunk)


	# Generate a chunk at given coordinates using pnoise2 and adding it to the chunk list
	def generate(self, chunkx, chunky):

		GRASS = "#"
		MOUNTAIN = "@"
		EMPTY = "."

		oct = 1

		floor_void_diff = 0.3
		mountain = 0.5

		floor = str()
		items = str()
		chunkname = str(chunkx) + "," + str(chunky)

		if chunkname not in self.chunks:
			# print("Generating chunk at {}".format(chunkname))
			for y in range(chunky * CHUNKSIZE, chunky * CHUNKSIZE + CHUNKSIZE):
				for x in range(chunkx * CHUNKSIZE, chunkx * CHUNKSIZE + CHUNKSIZE):
					i = round(noise.pnoise2(x / 15, y / 15, octaves = oct), 5)
					if i >= floor_void_diff:
						if i > mountain:
							floor += MOUNTAIN
						else:
							floor += GRASS
						spawner = random.randint(0, 100)

						if spawner == 0:
							items += "i"
						elif spawner == 1:
							items += "A"
						else:
							items += EMPTY

					elif i < floor_void_diff:
						floor += EMPTY
						items += EMPTY
					else:
						floor += EMPTY
						items += EMPTY
				floor += ":"
				items += ':'

			self.chunks.update({chunkname : {"floor" : floor, "items" : items}})
			self.unsaved += 1
		# else:
		# 	print("Chunk at {} has already been generated".format(chunkname))



	# Saving generated chunk list to a file, so it can be loaded from there rather than re-generating everything again
	def save(self):
		f = open('map.json', 'w')
		if self.unsaved == 0:
			# print("Nothing needs to be saved")
			self.unsaved = 0
			f.write(str(self.chunks))
		else:
			f = open("map.json", 'w+')
			f.seek(0)
			f.truncate()
			f.write(str(self.chunks))
			# if self.unsaved == 1:
			# 	print("Saved {} chunk".format(self.unsaved))
			# else:
			# 	print("Saved {} chunks".format(self.unsaved))
			self.unsaved = 0
		f.close()

	# Load chunk at given coordinates
	def load(self, chunkx, chunky):
		cname = str(chunkx) + ',' + str(chunky)

		if cname not in self.chunks:
			print("Chunk at {} does not exist".format(cname))
		else:
			if cname not in self.loaded:

				# Add the chunk to the loaded chunks list
				self.loaded.append(cname)
				# print("Loading chunk at {}".format(cname))
				data = []
				floordata = []
				itemdata = []

				# Select the chunk acording to the coordinates given
				chunktoload = self.chunks[cname]


				# Generate a data bundle so it can be passed to the map loader
				for index, type in enumerate(chunktoload):
					if type == "floor":
						x = 0
						y = 0
						for tile in chunktoload[type]:

							if y < CHUNKSIZE:
								if x < CHUNKSIZE:
									floordata.append((tile, x + chunkx * CHUNKSIZE, y + chunky * CHUNKSIZE))
									x+=1
								else:
									y+=1
									x=0
					if type == "items":
						x = 0
						y = 0
						for item in chunktoload[type]:
							if y < CHUNKSIZE:
								if x < CHUNKSIZE:
									if item != '.':
										itemdata.append((item, x + chunkx * CHUNKSIZE, y + chunky * CHUNKSIZE))
									x+=1
								else:
									y+=1
									x=0

				data = [floordata, itemdata]
				return data

			else:
				# print("Chunk at {} has already been loaded".format(cname))
				pass

chunkmanager = Chunk()
