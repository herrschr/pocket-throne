from code.mapmanager import MapManager
from code.tile import Tile
from code.tilemap import TileMap
from code.unitmanager import UnitManager
import pygame

#Pygame-Init

screen = None

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print pos

def pygame_init():
    global screen
    print screen
    pygame.init()
    screen = pygame.display.set_mode((120, 120))
    screen.fill((200, 200, 200))
    pygame.display.update()

pygame_init()

# making fake map
_map = TileMap()
_map.name = "Test Map"

tile_0_0 = Tile(0, 0, "W")
tile_1_0 = Tile(1, 0, "W")
tile_2_0 = Tile(2, 0, "W")
tile_0_1 = Tile(0, 1, "D")
tile_1_1 = Tile(1, 1, "D")
tile_2_1 = Tile(2, 1, "D")
tile_0_2 = Tile(0, 2, "G")
tile_1_2 = Tile(1, 2, "G")
tile_2_2 = Tile(2, 2, "G")

_map.add_tile(tile_0_0)
_map.add_tile(tile_1_0)
_map.add_tile(tile_2_0)
_map.add_tile(tile_0_1)
_map.add_tile(tile_1_1)
_map.add_tile(tile_2_1)
_map.add_tile(tile_0_2)
_map.add_tile(tile_1_2)
_map.add_tile(tile_2_2)

# Manager initialization
_mapmanager = MapManager(_map)
_unitmanager = UnitManager("base")

print "DEBUG MAP: " + str(_mapmanager._map.tiles_at)

# game loop
while 1==1:
	# draw tiles
	for tile in _mapmanager._map.tiles:
		full_img_path = "img/" + tile._image_path
		gui_position = _mapmanager.pos_to_gui((tile.pos_x, tile.pos_y))
		image = pygame.image.load(full_img_path)
		screen.blit(image, gui_position)
	events()
	pygame.display.flip()

