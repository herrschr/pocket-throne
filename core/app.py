# import python libraries
import os, sys, imp

# import os-dependant libs
from pygame_sdl2 import pygame_sdl2

# import whole core manahers
from core.managers.eventmanager import EventManager
from core.managers.inputmanager import InputManager
from core.managers.gameloopmanager import GameLoopManager
from core.managers.pygamedrawingmanager import PygameDrawingManager
from core.managers.unitmanager import UnitManager
from core.managers.mapmanager import MapManager
from core.managers.guimanager import GuiManager
from core.managers.ingamemanager import IngameManager

from core.tools.maploader import MapLoader

# initialize pygame screen as global
global screen
screen = None
eventMgr = EventManager()

# sys manager initialisation
inputMgr = InputManager(eventMgr)
loopMgr = GameLoopManager(eventMgr)
pygameMgr = PygameDrawingManager(eventMgr)

# loading map
_map = MapLoader("mountain_stream").get_map()

# Manager initialization
unitMgr = UnitManager(eventMgr, _map, mod="base")
mapMgr = MapManager(eventMgr, _map)
guiMgr = GuiManager(eventMgr)
ingameMgr = IngameManager(eventMgr)

# add two players
ingameMgr.add_new_player("Player 1", (255, 0, 0))
ingameMgr.add_new_player("Player 2", (0, 0, 255))

# add some units
unitMgr.spawn_unit_at(1, "swordsman", (2, 9))
unitMgr.spawn_unit_at(1, "swordsman", (3, 9))
unitMgr.spawn_unit_at(1, "archer", (10, 6))

# start loop
loopMgr.run()
ingameMgr.start_game()

