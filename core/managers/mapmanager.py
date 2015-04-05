from core.entities.gamestate import GameState

class MapManager:
	_tilesize = 40
	_map = None
	has_selected_tile = False
	selected = None

	def __init__(self, tilemap):
		# set self._map
		if tilemap == None:
			return None
		self._map = tilemap
		# update map in gamestate
		GameState.set_actual_map(self._map)

	# set tile at given position tuple as selected
	def select_tile_at(self, (pos_x, pos_y)):
		self.selected = self._map.get_tile_at((pos_x, pos_y))
		if self.selected == None:
			self.has_selected_tile = False
			return None
		self.has_selected_tile = True
		return self.selected

	# revert tile selection
	def unselect_tile(self):
		self.has_selected_tile = False
		self.selected = None

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
