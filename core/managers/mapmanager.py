from core.entities.gamestate import GameState

class MapManager:
	_tilesize = 40
	_map = None

	def __init__(self, tilemap):
		# set self._map
		if tilemap == None:
			return None
		self._map = tilemap
		# update map in gamestate
		GameState.set_actual_map(self._map)

	# return the GUI position for a tile
	def pos_to_gui(self,(x,y)):
		gui_x = x * self._tilesize
		gui_y = y * self._tilesize
		return (gui_x, gui_y)
