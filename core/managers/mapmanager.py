from core.tools.maploader import MapLoader
from core.managers.filemanager import FileManager
from core.managers.eventmanager import EventManager
from core.entities.event import *
from core.lang.unique import Unique

class MapManager(Unique):
	_tilesize = 40
	_map = None
	_mod = "base"
	has_selected_tile = False
	selected_tile = None

	def __init__(self, map_name=None, mod="base"):
		# register in EventManager
		EventManager.register_listener(self)
		# set self._map
		self._mod = mod
		if map_name == None:
			return
		else:
			self.load_map(map_name)

	def load_map(self, map_name):
		tilemap = MapLoader(map_name, mod=self._mod).get_map()
		self._map = self.postload_map(tilemap)
		EventManager.fire(MapLoadedEvent(self._map))

	def postload_map(self, tilemap):
		# set terrain bridges
		tilemap.initialize_neighbortiles()
		for tile in tilemap.tiles:
			n_north = tile.get_neighbor("N")
			n_south = tile.get_neighbor("S")
			n_west = tile.get_neighbor("W")
			n_east = tile.get_neighbor("E")
			# WATER
			if tile.get_landscape() == "W":
				if n_north != "W":
					tile.image_override = "tile_water_ontop_grass.png"
			# SNOW
			if tile.get_landscape() == "S":
				if n_north == "G" or n_north == "F" or n_north == "M":
					tile.image_override = "tile_snow_north_grass.png"
				elif n_south == "G" or n_south == "F" or n_south == "M":
					tile.image_override = "tile_snow_south_grass.png"
		return tilemap

	def get_loaded_map(self):
		return self._map

	def load_tiles(self):
		pass

	# set tile at given position tuple as selected
	def select_tile_at(self, (pos_x, pos_y)):
		self.selected_tile = self._map.get_tile_at((pos_x, pos_y))
		if self.selected_tile == None:
			self.has_selected_tile = False
			return None
		self.has_selected_tile = True
		EventManager.fire(TileUnselectedEvent())
		EventManager.fire(TileSelectedEvent(self.selected_tile, (pos_x, pos_y)))
		return self.selected_tile

	# revert tile selection
	def unselect_tile(self):
		self.has_selected_tile = False
		self.selected = None
		EventManager.fire(TileUnselectedEvent())

	# translates a TileMap grid position into display size
	@classmethod
	def pos_to_gui(self,(x, y)):
		gui_x = x * self._tilesize
		gui_y = self._map.size_y - y * self._tilesize
		return (gui_x, gui_y)

	# translates a position into the TileMap grid
	@classmethod
	def gui_to_pos(self, (x, y)):
		pos_x = int(x / self._tilesize)
		pos_y = int(y / self._tilesize)
		return (pos_x, pos_y)

	def on_event(self, event):
		# trigger TileSelectedEvent on mouse click
		if isinstance(event, MouseClickedEvent):
			# get selected tile
			grid_pos = self.gui_to_pos(event.pos)
			# self.selected_tile = self._map.get_tile_at(grid_pos)
			# fire TileSelectedEvent
			# ev_tile_selected = TileSelectedEvent(self.selected_tile, grid_pos)
			# EventManager.fire(ev_tile_selected)
