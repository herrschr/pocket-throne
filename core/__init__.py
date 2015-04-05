# AUTO IMPORT
# entities
from entities.building import Building
from entities.tile import Tile
from entities.tilemap import TileMap
from entities.unit import Unit, Weapon

from entities.gamestate import GameState

# managers
from managers.mapmanager import MapManager
from managers.unitmanager import UnitManager
from managers.filemanager import FileManager
from managers.ingamemanager import IngameManager

# tools
from tools.maploader import MapLoader

# get game root directory on package initialization
def getGameRoot():
	import os
	return os.path.abspath(__file__ + "/../../")

# initialize file manager
game_root = getGameRoot()
FileManager.set_game_root(game_root)