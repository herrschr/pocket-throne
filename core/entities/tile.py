class Tile:
	_id = -1
	def __init__(self,x,y,landscape):
		self.pos_x = x
		self.pos_y = y
		self.landscape = landscape
		self._image_path = self.get_image_path()

	# returns the tiles sprite path in /img folder
	def get_image_path(self):
		# grass
		if (self.landscape == "G"):
			return "tile_grass.png"
		# dirt
		elif (self.landscape == "D"):
			return "tile_dirt.png"
		# water
		elif (self.landscape == "W"):
			return "tile_water.png"
		# mointains
		elif (self.landscape == "M"):
			return "tile_mountains.png"
		# forest
		elif (self.landscape == "F"):
			return "tile_forest.png"
		else:
			return None

	def get_position(self):
		return (self.pos_x, self.pos_y)

	def __repr__(self):
		return "<Tile lds=" + self.landscape + " pos=" + str(self.get_position()) + ">"
