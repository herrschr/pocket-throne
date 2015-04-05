# import libraries
import sys
import pygame

# import whole core package
from core import *

# initialize pygame & pygame screen
def pygame_init():
	global screen
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	screen.fill((255, 255, 255))
	pygame.display.update()

# INIT scripts
# initialize pygame
screen = None
pygame_init()

# making fake map class
_maploader = MapLoader("rostow")
_map = _maploader.get_map()

# Manager initialization
_mapmanager = MapManager(_map)
_unitmanager = UnitManager("base")
_ingamemanager = IngameManager()

# add two players
_ingamemanager.add_new_player("Player 1", (255, 0, 0))
_ingamemanager.add_new_player("Player 2", (0, 0, 255))

# add some units

_unitmanager.spawn_unit_at(1, "swordsman", (2, 9))
_unitmanager.spawn_unit_at(1, "archer", (10, 6))

# catch events from game loop and react to them
def events():
	for event in pygame.event.get():
		# on exit
		if event.type == pygame.QUIT:
			sys.exit()
		# on left mouse press
		elif event.type == pygame.MOUSEBUTTONDOWN:
			gui_pos = pygame.mouse.get_pos()
			tile_pos = MapManager.gui_to_pos(gui_pos)
			_mapmanager.select_tile_at(tile_pos)
			print "selected tile: " + str(tile_pos)

# GAME LOOP
while True:
	# draw tiles
	for tile in _map.tiles:
		full_img_path = FileManager.image_path() + tile._image_path
		gui_position = MapManager.pos_to_gui((tile.pos_x, tile.pos_y))
		image = pygame.image.load(full_img_path)
		screen.blit(image, gui_position)

	# draw selected tile overlay
	if (_mapmanager.has_selected_tile):
		selected_img_path = FileManager.image_path() + "tile_selected.png"
		selected_gui_pos = MapManager.pos_to_gui(_mapmanager.selected.get_position())
		selected_img = pygame.image.load(selected_img_path)
		screen.blit(selected_img, selected_gui_pos)

	# draw units
	for unit in _unitmanager._units:
		full_img_path = FileManager.image_path() + unit.image_path
		gui_position = MapManager.pos_to_gui((unit.pos_x, unit.pos_y))
		image = pygame.image.load(full_img_path)
		screen.blit(image, gui_position)

	# TODO: draw buildings

	# catch mouse events
	events()
	# redraw display
	pygame.display.flip()
