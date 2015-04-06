# import python libraries
import os, sys, imp

# import os-dependant libs
from core.lib.posix.pygame_sdl2 import pygame_sdl2

# import whole core package
from core import *

# initialize pygame screen as global
global screen
screen = None
eventMgr = EventManager()

inputMgr = InputManager(eventMgr)
loopMgr = GameLoopManager(eventMgr)
pygameMgr = PygameGuiManager(eventMgr)

# loading map
_map = MapLoader("highland_bridge").get_map()

# Manager initialization
unitMgr = UnitManager(eventMgr, _map, mod="base")
mapMgr = MapManager(eventMgr, _map)
ingameMgr = IngameManager(eventMgr)

# add two players
ingameMgr.add_new_player("Player 1", (255, 0, 0))
ingameMgr.add_new_player("Player 2", (0, 0, 255))

# add some units
unitMgr.spawn_unit_at(1, "swordsman", (2, 9))
unitMgr.spawn_unit_at(1, "archer", (10, 6))

# start loop
loopMgr.run()

