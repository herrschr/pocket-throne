import json
import os

from kivy.core.image import Image

from core.managers.locator import Locator
from core.managers.filemanager import FileManager

from core.entities.tile import Tile
from core.entities.tilemap import TileMap
from core.entities.city import City
from core.entities.unit import Unit
from core.entities.player import Player

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
		# fill players
		self.fill_players(json_map)
		# fill cities
		self.fill_cities(json_map)
		# fill units
		self.fill_units(json_map)
		# set MapLoader as initialized
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

		# add _map.tiles and _map.tile_at for each grid position
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

	# fill the player list of the TileMap
	def fill_players(self, json_map):
		player_lines = json_map["players"]
		players = []
		for player_row in player_lines:
			# load player properties from line in map json
			player_row_data = player_row.split(",")
			player_name = player_row_data[0]
			player_color_data = player_row_data[1].strip().split(" ")
			print(player_color_data)
			color_r = int(player_color_data[0])
			color_g = int(player_color_data[1])
			color_b = int(player_color_data[2])
			player_color = (color_r, color_g, color_b)
			player_fraction_name = None
			# also load fraction when set
			if len(player_row_data) > 2:
				player_fraction_name = player_row_data[2].strip()
			print("player fraction name=" + player_fraction_name)
			# create player entity
			new_player = Player()
			new_player.name = player_name
			new_player.color = player_color
			new_player._fraction_name = player_fraction_name
			players.append(new_player)
		self._map.players = players

	# fill the city list of the TileMap class
	def fill_cities(self, json_map):
		city_lines = json_map["cities"]
		cities = []
		for city_row in city_lines:
			city_row_data = city_row.split(",")
			player_id = int(city_row_data[0])
			city_size = int(city_row_data[1])
			city_pos = (int(city_row_data[2]), int(city_row_data[3]))
			if len(city_row_data) > 4:
				city_name = city_row_data[4]
			# create new city
			city = City()
			city.playerId = player_id
			city.set_position(city_pos)
			city.set_size(city_size)
			if city_name:
				city.set_name(city_name)
			# add wall & stables
			city.add_city_wall()
			city.add_building("stables")
			cities.append(city)
		self._map.cities = cities

	# fill the unit list of the TileMap
	def fill_units(self, json_map):
		unit_lines = json_map["units"]
		units = []
		for unit_row in unit_lines:
			unit_row_data = unit_row.split(",")
			player_num = int(unit_row_data[0])
			unit_type = unit_row_data[1].strip()
			unit_pos = (int(unit_row_data[2]), int(unit_row_data[3]))
			# create new Unit
			unit = Unit(unit_type)
			unit.player_num = player_num
			unit.set_position(unit_pos)
			units.append(unit)
		self._map.units = units

	# returns the loaded map
	def get_map(self):
		if self._initialized:
			return self._map
		else:
			print ("[MapLoader] Error: map is null!")
			return None
