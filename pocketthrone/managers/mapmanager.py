__all__ = ('MapManager')

from pocketthrone.tools.maploader import MapLoader
from pocketthrone.managers.pipe import L
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.entities.event import *
from pocketthrone.entities.enum import TileLandscape, TileBiome, Compass

class MapManager:
	_tag = "[MapManager] "

	initialized = False

	has_selected_tile = False
	selected_tile = None
	tilemap = None

	enable_postloading = True
	enable_land_elevation = True
	enable_terrain_bridges = False

	# actual scrolling of the map
	viewport = []
	tiles_in_viewport = {}
	tiles_in_viewport_incomplete = False

	last_scrolling = {"x": None, "y": None}
	scrolling = {"x": 0, "y": 0}

	# number of tiles that are fitting in the map size
	grid_width = 0
	grid_height = 0

	def __init__(self, map_name=None):
		# register in EventManager
		EventManager.register(self)
		# set self._map; abort when none
		if map_name == None:
			print(self._tag + "ABORT map name to load = None")
		else:
			self.load_map(map_name)
			self.postload_map()

	def initialize(self):
		'''flag as initialized'''
		self.initialized = True

	def abort_when_uninitialized(self):
		'''abort method when uninitialized'''
		print(self._tag + "ABORT. ")

	def load_map(self, map_name):
		'''loads a map by its name'''
		if self.initialized:
			return
		# get selected mod & map
		selected_mod = L.ModManager.get_selected_mod()
		tilemap = MapLoader(map_name=map_name).get_tilemap()
		# set map in Locator and fire MapLoadedEvent
		if tilemap:
			print(self._tag + "SUCCESS MAP " + map_name + " loaded. Is now initialized.")
			# TileMap postloading
			self.tilemap = tilemap
			L.TileMap = tilemap
			# flag WidgetManager as initialized return TileMap
			self.initialized = True
			EventManager.fire(MapLoadedEvent(tilemap))

	def postload_map(self):
		'''tweak the TileMap after loading it with MapLoader (not neccessary)'''
		# set terrain bridges in map
		self.tilemap._initialize_neighbors()
		continent_lds = ["G", "F", "M"]
		bridge_directions = [Compass.DIRECTION_NORTH, Compass.DIRECTION_SOUTH]
		# override image paths on bridge tiles
		if self.enable_postloading:
			elev_counter = 0
			bridge_counter = 0
			print(self._tag + "POSTLOADING is on")
			for tile in self.tilemap.tiles:
				# LAND ELEVATION
				if self.enable_land_elevation:
					water_tiles = ["W", "=", "H"]
					counter = 0
					if tile.get_landscape() == TileLandscape.LANDSCAPE_WATER:
						print(self._tag + "self " + tile.get_landscape())
						neighbor_north = tile.get_neighbor(Compass.DIRECTION_NORTH)
						if neighbor_north and neighbor_north not in water_tiles:
							print(self._tag + tile.get_neighbor(Compass.DIRECTION_NORTH))
							tile.image_override = "tile_w_north_g"
							elev_counter += 1
						else:
							print("water on water")
				# TERRAIN BRIDGES
				if self.enable_terrain_bridges:
					if tile.get_landscape() == TileLandscape.LANDSCAPE_SNOW:
						if tile.get_neighbor(Compass.DIRECTION_NORTH) != TileLandscape.LANDSCAPE_SNOW:
							tile.image_override = "tile_s_north_g"
						elif tile.get_neighbor(Compass.DIRECTION_SOUTH) != TileLandscape.LANDSCAPE_SNOW:
							tile.image_override = "tile_s_south_g"
			print(self._tag + str(elev_counter) + " water elevation tiles")

	def get_tilemap(self):
		'''returns the TileMap instance of this game'''
		return self.tilemap

	def get_scrolling(self):
		'''returns the actual scrolling offset'''
		return self.scrolling

	def scroll(self, (rel_x, rel_y)):
		'''scrolls by relative position'''
		mapwidget = L.WidgetManager.get_widget("mapwidget")
		mapwidget.scroll((rel_x, rel_y))

	def scroll_at(self, (grid_x, grid_y)):
		'''scrolls at given grid position'''
		mapwidget = L.WidgetManager.get_widget("mapwidget")
		mapwidget.scroll_at((grid_x, grid_y))

	def select_tile_at(self, (pos_x, pos_y)):
		'''set tile at given position tuple as selected'''
		self.selected_tile = self.get_tile_at((pos_x, pos_y))
		# return None when tile isn't in map
		if self.selected_tile == None:
			self.has_selected_tile = False
			return None
		# set has_selected_tile flag
		self.has_selected_tile = True
		# fire TileUnselectedEvent
		EventManager.fire(TileUnselectedEvent())
		# fire TileSelectedEvent
		EventManager.fire(TileSelectedEvent(self.selected_tile, (pos_x, pos_y)))
		# return selected tile
		return self.selected_tile

	def get_tile_at(self, (pos_x, pos_y)):
		'''returns tile at given position tuple'''
		return self.tilemap.get_tile_at((pos_x, pos_y))

	def get_selected_tile(self):
		'''returns selected tile'''
		return self.selected_tile

	def has_selected_tile(self):
		'''returns whether a tile is selected'''
		if self.selected_tile == None:
			return False
		return True

	def unselect_tile(self):
		'''unselects selected tile'''
		self.has_selected_tile = False
		self.selected = None
		EventManager.fire(TileUnselectedEvent())

	def on_event(self, event):
		# map was scrolled after user input
		if isinstance(event, MapScrolledEvent):
			# update previous scrolling cache
			prev_scrolling = {"x": int(event.prev_x), "y": int(event.prev_y)}
			new_scrolling = {"x": int(event.new_x), "y": int(event.new_y)}
			# update scrolling cache
			self.prev_scrolling = prev_scrolling
			self.scrolling = new_scrolling
