import json
import os
from random import seed, choice

from kivy.core.image import Image

from pocketthrone.managers.locator import Locator
from pocketthrone.managers.filemanager import FileManager

from pocketthrone.entities.tile import Tile
from pocketthrone.entities.tilemap import TileMap
from pocketthrone.entities.city import City
from pocketthrone.entities.unit import Unit
from pocketthrone.entities.player import Player

class MapLoader:
	_tag = "[MapLoader] "
	is_initialized = False
	tilemap = None

	_rnd_buildings = ["stables", "market"]

	def __init__(self, map_name=None):
		print(self._tag + "load map " + map_name + "...")
		# load map file into jsontilemap json dict
		selected_mod_name = Locator.MOD_MGR.get_selected_mod()._basename
		print (self._tag + "mod is " + selected_mod_name)
		if selected_mod_name == None or selected_mod_name == "":
			print(self._tag + "mod is NONE")
			return None
		map_path = FileManager.mod_path() + selected_mod_name + "/maps/" + map_name + ".json"
		map_string = FileManager.read_file(map_path)
		if (map_string == ""):
			return None
		json_tilemap = json.loads(map_string)
		# create and fill TileMap
		# fill map name and size
		self.tilemap = TileMap()
		self.tilemap._name = map_name
		self.fill_properties(json_tilemap)
		# fill map tiles
		self.fill_tiles(json_tilemap)
		# fill players
		self.fill_players(json_tilemap)
		# fill cities
		self.fill_cities(json_tilemap)
		# fill units
		self.fill_units(json_tilemap)
		# set MapLoader as initialized
		self.is_initialized = True

	# fill map properties for self.tilemap
	def fill_properties(self, json_tilemap):
		self.tilemap.name = json_tilemap["name"]
		self.tilemap.name_de = json_tilemap["name_de"]
		self.tilemap.size_x = int(json_tilemap["size"].split("x")[0])
		self.tilemap.size_y = int(json_tilemap["size"].split("x")[1])

	# fill tiles for self.tilemap
	def fill_tiles(self, json_tilemap):
		# get tiletilemap string and real map size
		row_array = json_tilemap["tile_map"]
		size_x = self.tilemap.size_x
		size_y = self.tilemap.size_y

		# add tilemap.tiles and tilemap.tile_at for each grid position
		cursor_x = 0
		cursor_y = 0
		while cursor_y < size_y:
			row = row_array[cursor_y]
			while cursor_x < size_x:
				pos_x = cursor_x
				pos_y = cursor_y
				landscape = row[cursor_x]
				tile = Tile(pos_x, pos_y, landscape)
				self.tilemap.add_tile(tile)
				cursor_x += 1
			cursor_x = 0
			cursor_y += 1

	# fill the player list of the TileMap
	def fill_players(self, json_tilemap):
		player_lines = json_tilemap["players"]
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
		self.tilemap.players = players

	# fill the city list of the TileMap class
	def fill_cities(self, json_tilemap):
		city_lines = json_tilemap["cities"]
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
			seed()
			random_building = choice(self._rnd_buildings)
			city.add_building(random_building)
			cities.append(city)
		self.tilemap.cities = cities

	# fill the unit list of the TileMap
	def fill_units(self, json_tilemap):
		unit_lines = json_tilemap["units"]
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
		self.tilemap.units = units

	# returns the loaded map
	def get_tilemap(self):
		if self.is_initialized:
			return self.tilemap
		else:
			print ("[MapLoader] Error: map is null!")
			return None
