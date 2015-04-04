# IMPORTS
# user lib & system lib import
import pygame

# manager imports
from core.managers.mapmanager import MapManager
from core.managers.unitmanager import UnitManager

# entity imports
from core.entities.tile import Tile
from core.entities.tilemap import TileMap

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
	screen = pygame.display.set_mode((120, 120))
	screen.fill((200, 200, 200))
	pygame.display.update()

# INIT scripts
# initialize pygame
screen = None
pygame_init()

# making fake map class
_map = TileMap()
_map.name = "Test Map"

# manually create tiles and add them to map
_map.add_tile(Tile(0, 0, "W"))
_map.add_tile(Tile(1, 0, "W")
_map.add_tile(Tile(2, 0, "W"))
_map.add_tile(Tile(0, 1, "D"))
_map.add_tile(Tile(1, 1, "D"))
_map.add_tile(Tile(2, 1, "D"))
_map.add_tile(Tile(0, 2, "G"))
_map.add_tile(Tile(1, 2, "G"))
_map.add_tile(Tile(2, 2, "G"))

# Manager initialization
_mapmanager = MapManager(_map)
_unitmanager = UnitManager("base")

# GAME LOOP
while 1==1:
	# draw tiles
	for tile in _mapmanager._map.tiles:
		full_img_path = "img/" + tile._image_path
		gui_position = _mapmanager.pos_to_gui((tile.pos_x, tile.pos_y))
		image = pygame.image.load(full_img_path)
		screen.blit(image, gui_position)
	# catch mouse event
	events()
	# redraw display
	pygame.display.flip()

