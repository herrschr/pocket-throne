import pygame
from core.entities.gamestate import GameState

class MapManager:
	_tilesize = 40
	_map = None

	def __init__(self, tilemap):
		# set self._map
		if tilemap == None:
			return None
		self._map = tilemap
		GameState.set_actual_map(self._map)

	def pos_to_gui(self,(x,y)):
		gui_x = x * self._tilesize
		gui_y = y * self._tilesize
		return (gui_x, gui_y)

	def spawn_unit(self,x,y):
		pass

	def move_unit(self):
		pass

	def spawn_building(self, building,x,y):
		if building == None:
			pass
		else:
			image = pygame.image.load(building.image)
			screen.blit(image, pos_to_gui(x,y))
