# -*- coding: utf-8 -*-

class Tile:
	# sys properties
	_id = -1
	_neighbor_west = None
	_neighbor_north = None
	_neighbor_east = None
	_neighbor_south = None

	# tile path & name constants
	image_override = None
	image_paths = {
		"G": "tile_grass.png",
		"D": "tile_dirt.png",
		"W": "tile_water.png",
		"M": "tile_mountains.png",
		"F": "tile_forest.png"}
	names = {
		"G": "Green Grasslands",
		"D": "Dirty Landscapes",
		"W": "The Sea",
		"M": "High Mountains",
		"F": "A Dark Forest"}
	names_de = {
		"G": "Grüne Wiesen",
		"D": "Dürre Erde",
		"W": "Wasser",
		"M": "Hohe Berge",
		"F": "Düsterer Wald"}
	walkable = {"G": True, "D": True, "W": False, "M": False, "F": True}

	def __init__(self,x,y,landscape=None):
		self.pos_x = x
		self.pos_y = y
		self.landscape = landscape
		self.name = self.get_name()
		self._image_path = self.get_image_path()

	# returns the tiles sprite path in /img folder
	def get_image_path(self):
		if self.image_override:
			return self.image_override
		return self.image_paths.get(self.landscape, None)

	def get_name(self):
		return self.names.get(self.landscape, None)

	def get_name_de(self):
		return self.names_de.get(self.landscape, None)

	def is_walkable(self):
		return self.walkable.get(self.landscape, True)

	def get_landscape(self):
		return self.landscape

	def get_position(self):
		return (self.pos_x, self.pos_y)

	def __repr__(self):
		return "<Tile lds=" + self.landscape + " pos=" + str(self.get_position()) + ">"
