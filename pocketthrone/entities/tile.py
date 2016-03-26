# -*- coding: utf-8 -*-
from kivy.core.image import Image as CoreImage

from pocketthrone.entities.enum import TileLandscape, TileBiome, Compass

class Tile:
	# sys properties
	_tag = "[Tile] "
	_id = -1
	name = None

	# default texture path
	texture_names = {
		"G": "tile_g",
		"D": "tile_d",
		"W": "tile_w",
		"M": "tile_m",
		"F": "tile_f",
		"S": "tile_s",
		"H": "tile_h"}

	# english tile names
	names = {
		"G": "Green Grasslands",
		"D": "Dirty Landscapes",
		"W": "The Sea",
		"M": "High Mountains",
		"F": "A Dark Forest",
		"S": "Cold Snow",
		"H": "Bridge",
		"=": "Bridge"}

	# german human readable Tile name descriptions
	names_de = {
		"G": "Grüne Wiesen",
		"D": "Dürre Erde",
		"W": "Wasser",
		"M": "Hohe Berge",
		"F": "Düsterer Wald",
		"S": "Eisige Kälte",
		"H": "Brücke",
		"=": "Brücke"}

	walkable = {"G": True, "D": True, "W": False, "M": False, "F": True, "S": True}

	pos_x = -1
	pos_y = -1

	def __init__(self,x,y,landscape=None):
		# texture path override
		self.image_override = None
		self.texture_name = None
		self.neighbors = {}
		self.landscape = None
		# set position
		self.pos_x = x
		self.pos_y = y
		# set name & landscape
		self.landscape = landscape
		self.name = self.get_name()
		# initialize image path
		self._texture_name = "none.png"

	def get_texture_name(self):
		'''returns the tiles sprite path in /img folder'''
		lds = unicode(self.landscape)
		if self.image_override != None:
			return self.image_override
		texture_name = "tile_" + unicode.lower(lds)
		# make texture pat
		return texture_name

	def get_neighbor(self, compass):
		'''returns the neighbor Tile in Compass direction; else returns None'''
		try:
			return self.neighbors[compass]
		except Exception:
			return None

	def get_name(self):
		'''returns English name of this Tile\'s landscape'''
		return self.names.get(self.landscape, None)

	def get_name_de(self):
		'''returns German name of this Tile\'s landscape'''
		return self.names_de.get(self.landscape, None)

	def is_walkable(self):
		'''returns if tile is walkable by land units'''
		return self.walkable.get(self.landscape, True)

	def get_landscape(self):
		'''returns landscape of this tile'''
		return self.landscape

	def set_landscape(self, lds):
		self.landscape = lds

	def get_position(self):
		'''returns position of this tile'''
		return (self.pos_x, self.pos_y)

	def get_x(self):
		'''returns horizontal position of this tile'''
		return self.pos_x

	def get_y(self):
		'''returns vertical position of this tile'''
		return self.pos_y

	def __repr__(self):
		'''returns xml like representation of this tile'''
		return "<Tile lds=" + self.landscape + " pos=" + str(self.get_position()) + ">"
