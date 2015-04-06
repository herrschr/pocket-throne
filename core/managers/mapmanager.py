from core.entities.gamestate import GameState
from core.entities.event import *

class MapManager:
	_tilesize = 40
	_map = None
	has_selected_tile = False
	selected = None

	def __init__(self, eventmanager, tilemap):
		# register in EventManager
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)
		# set self._map
		if tilemap == None:
			return None
		self._map = tilemap
		self._eventmgr.post(MapLoadedEvent(self._map))
		# update map in gamestate
		GameState.set_actual_map(self._map)

	# set tile at given position tuple as selected
	def select_tile_at(self, (pos_x, pos_y)):
		self.selected = self._map.get_tile_at((pos_x, pos_y))
		if self.selected == None:
			self.has_selected_tile = False
			return None
		self.has_selected_tile = True
		self._eventmgr.post(TileSelectedEvent(self.selected))
		return self.selected

	# revert tile selection
	def unselect_tile(self):
		self.has_selected_tile = False
		self.selected = None
		self._eventmgr.post(TileUnselectedEvent())

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
			ev_tile_selected = TileSelectedEvent(selected_tile)
			self._eventmgr.post(ev_tile_selected)
