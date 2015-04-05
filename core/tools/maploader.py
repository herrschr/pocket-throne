import json
import os

from core.managers.filemanager import FileManager

from core.entities.tile import Tile
from core.entities.tilemap import TileMap
from core.entities.building import Building
from core.entities.unit import Unit

class MapLoader:
	_initialized = False
	_map = None

	def __init__(self, map_name):
		# load map file into json_map json dict
		map_path = FileManager.mod_path() + "base/maps/" + map_name + ".json"
		map_string = FileManager.read_file(map_path)
		if (map_string == ""):
			return None
		json_map = json.loads(map_string)

		# create and fill TileMap
		self._map = TileMap()
		self.fill_map_properties(json_map)
		self.fill_map_tiles(json_map)
		self._initialized = True

	# fill map properties for self._map
	def fill_map_properties(self, json_map):
		self._map.name = json_map["name"]
		self._map.size_x = int(json_map["size"].split("x")[0])
		self._map.size_y = int(json_map["size"].split("x")[1])

	# fill tiles for self._map
	def fill_map_tiles(self, json_map):
		# get tile_map string and real map size
		row_array = json_map["tile_map"]
		size_x = self._map.size_x
		size_y = self._map.size_y

		# add _map.tiles and _map.tile_at
		cursor_x = 0
		cursor_y = 0
		while cursor_y < size_y:
			row = row_array[cursor_y]
			while cursor_x < size_x:
				pos_x = cursor_x
				pos_y = cursor_y
				landscape = row[cursor_x]
				tile = Tile(pos_x, pos_y, landscape)
				self._map.add_tile(tile)
				cursor_x += 1
			cursor_x = 0
			cursor_y += 1

	# returns the loaded map
	def get_map(self):
		if self._initialized:
			return self._map
		else:
			print "Error: map is null!"
			return None
