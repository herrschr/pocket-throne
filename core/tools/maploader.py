import json
import os

from kivy.core.image import Image

from core.managers.filemanager import FileManager

from core.entities.tile import Tile
from core.entities.tilemap import TileMap
from core.entities.city import City
from core.entities.unit import Unit

class MapLoader:
	_initialized = False
	_map = None
	_textures = {}

	def __init__(self, map_name, mod="base"):
		# load map file into json_map json dict
		map_path = FileManager.mod_path() + mod + "/maps/" + map_name + ".json"
		map_string = FileManager.read_file(map_path)
		if (map_string == ""):
			return None
		json_map = json.loads(map_string)
		# create and fill TileMap
		# fill map name and size
		self._map = TileMap()
		self._map._name = map_name
		self.fill_map_properties(json_map)
		# fill map tiles
		self.fill_map_tiles(json_map)
		# fill buildings
		self.fill_cities(json_map)
		self._initialized = True

	# fill map properties for self._map
	def fill_map_properties(self, json_map):
		self._map.name = json_map["name"]
		self._map.name_de = json_map["name_de"]
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

	# fill the city list of the TileMap class
	def fill_cities(self, json_map):
		city_lines = json_map["cities"]
		cities = []
		for city_row in city_lines:
			city_row_data = city_row.split()
			player_id = int(city_row_data[0])
			city_size = int(city_row_data[1])
			city_pos = (int(city_row_data[2]), int(city_row_data[3]))
			# create new city
			city = City()
			city.playerId = player_id
			city.set_position(city_pos)
			city.set_size(city_size)
			cities.append(city)
		self._map.cities = cities
		print("cities: " + str(self._map.cities))

	# returns the loaded map
	def get_map(self):
		if self._initialized:
			return self._map
		else:
			print ("Error: map is null!")
			return None
