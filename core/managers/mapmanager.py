from core.tools.maploader import MapLoader
from core.managers.filemanager import FileManager
from core.entities.event import *

class MapManager:
	_tilesize = 40
	_map = None
	has_selected_tile = False
	selected = None

	def __init__(self, eventmanager, map_name=None, mod="base"):
		# register in EventManager
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)
		# set self._map
		if map_name == None:
			return
		else:
			self.load_map(map_name)

	def load_map(self, map_name):
		tilemap = MapLoader(map_name).get_map()
		self._map = self.postload_map(tilemap)
		self._eventmgr.fire(MapLoadedEvent(self._map))

	def postload_map(self, tilemap):
		# set terrain bridges
		tilemap.initialize_neighbortiles()
		for tile in tilemap.tiles:
			if tile.get_landscape() == "W":
				if tile._neighbor_north == "G" or tile._neighbor_north == "M":
					tile.image_override = "tile_water_ontop_grass.png"
		return tilemap

	def get_loaded_map(self):
		return self._map

	def load_tiles(self):
		pass

	# set tile at given position tuple as selected
	def select_tile_at(self, (pos_x, pos_y)):
		self.selected = self._map.get_tile_at((pos_x, pos_y))
		if self.selected == None:
			self.has_selected_tile = False
			return None
		self.has_selected_tile = True
		self._eventmgr.fire(TileSelectedEvent(self.selected))
		return self.selected

	# revert tile selection
	def unselect_tile(self):
		self.has_selected_tile = False
		self.selected = None
		self._eventmgr.fire(TileUnselectedEvent())

	# translates a TileMap grid position into display size
	@classmethod
	def pos_to_gui(self,(x, y)):
		gui_x = x * self._tilesize
		gui_y = y * self._tilesize
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
			selected_tile = self._map.get_tile_at(grid_pos)
			# fire TileSelectedEvent
			ev_tile_selected = TileSelectedEvent(selected_tile, grid_pos)
			self._eventmgr.fire(ev_tile_selected)
