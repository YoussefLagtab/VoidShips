import noise
from settings import *
import pickle

class Chunk():

	def __init__(self):

		try:
			with open("map.pickle", 'rb') as f:
				self.chunks = pickle.load(f)
		except:
			with open('map.pickle', 'wb') as f:
				self.chunks = {}
				pickle.dump(self.chunks, f)

		with open("map.pickle", 'rb') as f:
			self.chunks = pickle.load(f)

		self.loaded = []
		self.chunk = tuple()
		self.unsaved = int()

	def get_chunks(self):
		return self.chunks

	def get_loaded(self):
		return self.loaded

	# remove given chunk from the loaded list, so it does not affect the performance
	def unload(self, chunk):
		self.loaded.remove(chunk)

	def kill_item(self, chunk, pos):
		if self.chunks[chunk]['items'][pos]:
			del self.chunks[chunk]['items'][pos]
		else:
			print('Item does not exist')
			pass



	# Generate a chunk at given coordinates using pnoise2 and adding it to the chunk list
	def generate(self, chunkx, chunky):

		GRASS = "#"
		MOUNTAIN = "@"
		EMPTY = "."

		oct = 1

		floor_void_diff = 0.3
		mountain = 0.5

		floor = str()
		items = {}
		chunk = (chunkx, chunky)

		if chunk not in self.chunks:

			# print("Generating chunk at {}".format(chunk))
			for y in range(chunky * CHUNKSIZE, chunky * CHUNKSIZE + CHUNKSIZE):
				for x in range(chunkx * CHUNKSIZE, chunkx * CHUNKSIZE + CHUNKSIZE):
					i = round(noise.pnoise2(x / 15, y / 15, octaves = oct), 5)
					if i >= floor_void_diff:
						if i > mountain:
							floor += MOUNTAIN
						else:
							floor += GRASS
						spawner = random.randint(0, 1)

						if spawner == 0:
							items.update({(x, y) : "i"})
						elif spawner == 1:
							items.update({(x, y) : "A"})

					elif i < floor_void_diff:
						floor += EMPTY
					else:
						floor += EMPTY
				floor += ":"

			self.chunks.update({chunk : {"floor" : floor, "items" : items}})
			self.unsaved += 1
		# else:
		# 	print("Chunk at {} has already been generated".format(chunk))



	# Saving generated chunk list to a file, so it can be loaded from there rather than re-generating everything again
	def save(self):
		f = open('map.pickle', 'wb')
		if self.unsaved == 0:
			print("Nothing needs to be saved")
			self.unsaved = 0
			pickle.dump(self.chunks, f)
		else:
			f = open("map.pickle", 'wb')
			pickle.dump(self.chunks, f)
			if self.unsaved == 1:
				print("Saved {} chunk".format(self.unsaved))
			else:
				print("Saved {} chunks".format(self.unsaved))
			self.unsaved = 0
		f.close()

	# Load chunk at given coordinates
	def load(self, chunkx, chunky):
		chunk = (chunkx, chunky)

		if chunk not in self.chunks:
			print("Chunk at {} does not exist".format(cname))
		else:
			if chunk not in self.loaded:

				# Add the chunk to the loaded chunks list
				self.loaded.append(chunk)
				# print("Loading chunk at {}".format(cname))
				data = []
				floordata = []
				itemdata = []

				# Select the chunk acording to the coordinates given
				chunktoload = self.chunks[chunk]


				# Generate a data bundle so it can be passed to the map loader
				for index, type in enumerate(chunktoload):
					if type == "floor":
						x = 0
						y = 0
						for tile in chunktoload['floor']:

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
						for item in chunktoload['items']:
							itemdata.append((chunktoload['items'][item], item[0], item[1]))

				data = [floordata, itemdata]
				return data

			else:
				# print("Chunk at {} has already been loaded".format(cname))
				pass

chunkmanager = Chunk()
