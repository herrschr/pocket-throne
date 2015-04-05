# AUTO IMPORT
# entities
from core.entities.building import Building
from core.entities.tile import Tile
from core.entities.tilemap import TileMap
from core.entities.unit import Unit, Weapon

from core.entities.event import *
from core.entities.gamestate import GameState

# managers
from core.managers.eventmanager import EventManager
from core.managers.gameloopmanager import GameLoopManager

from core.managers.inputmanager import InputManager
from core.managers.ingamemanager import IngameManager
from core.managers.pygameguimanager import PygameGuiManager

from core.managers.mapmanager import MapManager
from core.managers.unitmanager import UnitManager
from core.managers.filemanager import FileManager

# tools
from tools.maploader import MapLoader

# get game root directory on package initialization
def getGameRoot():
	import os
	return os.path.abspath(__file__ + "/../../")

# initialize file manager
game_root = getGameRoot()
FileManager.set_game_root(game_root)