# AUTO IMPORT
# entities
from entities.building import Building
from entities.tile import Tile
from entities.tilemap import TileMap
from entities.unit import Unit, Weapon

# managers
from managers.mapmanager import MapManager
from managers.unitmanager import UnitManager
from managers.filemanager import FileManager

def getGameRoot():
	import os
	return os.path.abspath(__file__ + "/../../")

# initialize file manager
game_root = getGameRoot()
FileManager.set_game_root(game_root)