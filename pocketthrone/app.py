# import python libraries
import os, sys, imp

# import kivy
import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView

# import whole core managers
from pocketthrone.entities.mod import Mod
from pocketthrone.entities.tile import Tile
from pocketthrone.entities.event import *
from pocketthrone.managers.locator import Locator
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.managers.inputmanager import InputManager
from pocketthrone.managers.gameloopmanager import GameLoopManager
from pocketthrone.managers.modmanager import ModManager
from pocketthrone.managers.unitmanager import UnitManager
from pocketthrone.managers.citymanager import CityManager
from pocketthrone.managers.mapmanager import MapManager
from pocketthrone.managers.guimanager import GuiManager
from pocketthrone.managers.playermanager import PlayerManager

from pocketthrone.gui.mapwidget import MapWidget
from pocketthrone.gui.bottombar import BottomBar
from pocketthrone.gui.sidebar import SideBar
from pocketthrone.tools.maploader import MapLoader

class PocketThroneApp(App):
	def build(self):
		self.initialize_managers()

		# create GUI
		root = FloatLayout(pos=(0,0), size=(Window.size))
		Locator.GUI_MGR.register_widget("root", root)
		mapwidget = MapWidget()
		bottombar = BottomBar()

		root.add_widget(mapwidget)
		root.add_widget(bottombar)
		return root

	def initialize_managers(self):
		# set mod and map to load here
		_mod_name = "westeros"
		_map_name = "westeros"

		# set basic managers in Locator class
		Locator.MOD_MGR = ModManager(mod_name = _mod_name)
		Locator.GUI_MGR = GuiManager()
		Locator.INPUT_MGR = InputManager()
		Locator.GAMELOOP_MGR = GameLoopManager()

		# Manager initialization inside Locator holder class
		Locator.PLAYER_MGR = PlayerManager()
		Locator.MAP_MGR = MapManager(map_name=_map_name)
		Locator.TILEMAP = Locator.MAP_MGR.get_tilemap()
		Locator.UNIT_MGR = UnitManager()
		Locator.CITY_MGR = CityManager()

		# start loop & first turn
		Locator.GAMELOOP_MGR.run()
		Locator.PLAYER_MGR.start_game()

