class Tile:
	_id = -1

	image_paths = {
		"G": "tile_grass.png",
		"D": "tile_dirt.png",
		"W": "tile_water.png",
		"M": "tile_mountains.png",
		"F": "tile_forest.png"
	}

	names = {
		"G": "Green Grasslands",
		"D": "Dirty Landscapes",
		"W": "The Sea",
		"M": "High Mountains",
		"F": "A Dark Forest"
	}

	def __init__(self,x,y,landscape):
		self.pos_x = x
		self.pos_y = y
		self.landscape = landscape
		self.name = self.get_name()
		self._image_path = self.get_image_path()

	# returns the tiles sprite path in /img folder
	def get_image_path(self):
		return self.image_paths.get(self.landscape, None)

	def get_name(self):
		return self.names.get(self.landscape, None)

	def get_position(self):
		return (self.pos_x, self.pos_y)

	def __repr__(self):
		return "<Tile lds=" + self.landscape + " pos=" + str(self.get_position()) + ">"
