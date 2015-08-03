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

class PocketLordApp(App):
	def build(self):
		self.initialize_managers()
		# create MapWidget in Scatter for free movement
		mapwidget = MapWidget(size=(Locator.TILEMAP.size_x *40, Locator.TILEMAP.size_y *40))
		# create GUI
		bottombar = BottomBar()
		sidebar_scroller = ScrollView(do_scroll_x=False, size_hint=(.2, .8), pos=(0, 100), bar_pos_y="left", bar_width=20)
		sidebar = SideBar()
		sidebar_scroller.add_widget(sidebar)
		# add all to root layout
		root = FloatLayout(pos=(0,0), size=(Window.size))
		root.add_widget(mapwidget)
		root.add_widget(bottombar)
		root.add_widget(sidebar_scroller)

		# add layouts to GuiManager and return root
		Locator.GUI_MGR.root = root
		Locator.GUI_MGR.bottombar = bottombar
		Locator.GUI_MGR.sidebar = sidebar
		Locator.GUI_MGR.mapwidget = mapwidget
		return root

	def initialize_managers(self):
		Locator.INPUT_MGR = InputManager()
		Locator.GAMELOOP_MGR = GameLoopManager()

		# Manager initialization
		Locator.MAP_MGR = MapManager(map_name="westeros", mod="westeros")
		# initialize global managers
		Locator.TILEMAP = Locator.MAP_MGR.get_loaded_map()
		Locator.UNIT_MGR = UnitManager(Locator.TILEMAP, mod="westeros")
		Locator.CITY_MGR = CityManager(Locator.TILEMAP, mod="westeros")
		Locator.GUI_MGR = GuiManager()
		Locator.INGAME_MGR = IngameManager(mod="westeros")

		# add two players
		Locator.INGAME_MGR.add_new_player("Player 1", (255, 0, 0))
		Locator.INGAME_MGR.add_new_player("Player 2", (0, 0, 255))

		# add some units
		Locator.UNIT_MGR.spawn_unit_at(1, "soldier", (23, 23))
		Locator.UNIT_MGR.spawn_unit_at(1, "courier", (23, 24))
		Locator.UNIT_MGR.spawn_unit_at(2, "crossbowman", (30, 56))

		# start loop
		Locator.GAMELOOP_MGR.run()
		Locator.INGAME_MGR.start_game()

