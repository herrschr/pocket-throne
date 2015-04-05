# IMPORTS
# import libraries
import sys
import pygame
# import whole core package
from core import *

# METHODS
# catch events from game loop and react to them
def events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			print pos

# initialize pygame & pygame screen
def pygame_init():
	global screen
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	screen.fill((200, 200, 200))
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

# GAME LOOP
while 1==1:
	# draw tiles
	for tile in _map.tiles:
		full_img_path = "img/" + tile._image_path
		gui_position = _mapmanager.pos_to_gui((tile.pos_x, tile.pos_y))
		image = pygame.image.load(full_img_path)
		screen.blit(image, gui_position)

	# TODO: draw units
	# TODO: draw buildings

	# catch mouse event
	events()
	# redraw display
	pygame.display.flip()