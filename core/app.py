# import python libraries
import os, sys, imp

# import os-dependant libs
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from core.gui.mapwidget import MapWidget

# import whole core managers
from core.entities.tile import Tile
from core.entities.event import *
from core.managers.filemanager import FileManager
from core.managers.eventmanager import EventManager
from core.managers.inputmanager import InputManager
from core.managers.gameloopmanager import GameLoopManager
from core.managers.unitmanager import UnitManager
from core.managers.citymanager import CityManager
from core.managers.mapmanager import MapManager
from core.managers.guimanager import GuiManager
from core.managers.ingamemanager import IngameManager
from core.managers.locator import Locator

from core.tools.maploader import MapLoader
from core.gui.bottombar import BottomBar
from core.gui.sidebar import SideBar

import core.managers

class PocketThroneApp(App):
	def build(self):
		self.initialize_managers()
		# create MapWidget in Scatter for free movement
		mapwidget = MapWidget(size=(Locator.TILEMAP.size_x *40, Locator.TILEMAP.size_y *40))
		# create GUI
		bottombar = BottomBar()
		# add all to root layout
		root = FloatLayout(pos=(0,0), size=(Window.size))
		root.add_widget(mapwidget)
		root.add_widget(bottombar)

		# add layouts to GuiManager and return root
		Locator.GUI_MGR.root = root
		Locator.GUI_MGR.bottombar = bottombar
		Locator.GUI_MGR.mapwidget = mapwidget
		return root

	def initialize_managers(self):
		# set basic managers in Locator class
		Locator.INPUT_MGR = InputManager()
		Locator.GAMELOOP_MGR = GameLoopManager()

		# Manager initialization
		Locator.MAP_MGR = MapManager(map_name="westeros", mod="westeros")
		# initialize global managers in Locator class
		Locator.TILEMAP = Locator.MAP_MGR.get_loaded_map()
		Locator.UNIT_MGR = UnitManager(Locator.TILEMAP, mod="westeros")
		Locator.CITY_MGR = CityManager(Locator.TILEMAP, mod="westeros")
		Locator.GUI_MGR = GuiManager()
		Locator.INGAME_MGR = IngameManager(mod="westeros")

		# add two players
		Locator.INGAME_MGR.add_new_player("Rebellion", (255, 0, 0))
		Locator.INGAME_MGR.add_new_player("Loyalists", (0, 0, 255))

		# add some units
		Locator.UNIT_MGR.spawn_unit_at(2, "soldier", (23, 23))
		Locator.UNIT_MGR.spawn_unit_at(2, "courier", (23, 24))
		Locator.UNIT_MGR.spawn_unit_at(1, "crossbowman", (27, 56))

		# start loop
		Locator.GAMELOOP_MGR.run()
		Locator.INGAME_MGR.start_game()

