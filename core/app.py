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
from core.managers.playermanager import PlayerManager
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
		# set mod and map to load here
		_mod_name = "westeros"
		_map_name = "westeros"

		# set basic managers in Locator class
		Locator.INPUT_MGR = InputManager()
		Locator.GAMELOOP_MGR = GameLoopManager()

		# Manager initialization inside Locator holder class
		Locator.MAP_MGR = MapManager(map_name=_map_name, mod=_mod_name)
		Locator.TILEMAP = Locator.MAP_MGR.get_loaded_map()
		Locator.UNIT_MGR = UnitManager(Locator.TILEMAP, mod=_mod_name)
		Locator.CITY_MGR = CityManager(Locator.TILEMAP, mod=_mod_name)
		Locator.GUI_MGR = GuiManager()
		Locator.PLAYER_MGR = PlayerManager(mod=_mod_name)

		# add two players
		Locator.PLAYER_MGR.add_new_player("Rebellion", (255, 0, 0), fraction_name="stark")
		Locator.PLAYER_MGR.add_new_player("Loyalists", (0, 0, 255), fraction_name="lannister")

		# add some units
		Locator.UNIT_MGR.spawn_unit_at(2, "soldier", (23, 23))
		Locator.UNIT_MGR.spawn_unit_at(1, "archer", (27, 56))

		# start loop & first turn
		Locator.GAMELOOP_MGR.run()
		Locator.PLAYER_MGR.start_game()

