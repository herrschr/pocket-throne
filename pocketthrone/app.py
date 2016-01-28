# -*- coding: utf-8 -*-

# import python libraries
import os

# import kivy
import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

# import whole core managers
from pocketthrone.managers.locator import L
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.inputmanager import InputManager
from pocketthrone.managers.gameloopmanager import GameLoopManager
from pocketthrone.managers.modmanager import ModManager
from pocketthrone.managers.unitmanager import UnitManager
from pocketthrone.managers.citymanager import CityManager
from pocketthrone.managers.mapmanager import MapManager
from pocketthrone.managers.widgetmanager import WidgetManager
from pocketthrone.managers.playermanager import PlayerManager

# import entities
from pocketthrone.entities.unit import Unit
from pocketthrone.entities.tile import Tile
from pocketthrone.entities.building import Building
from pocketthrone.entities.event import *

# import widget classes
from pocketthrone.widgets.mapwidget import MapWidget
from pocketthrone.widgets.bottombar import BottomBar
from pocketthrone.widgets.sidebar import SideBar
from pocketthrone.tools.maploader import MapLoader

class PocketThroneApp(App):
	# set mod and map to load here
	MOD_NAME = "ancientlies"
	MAP_NAME = "highland_bridge"

	# auto-set display size before cstarting
	def build_config(self, config):
		config.setdefaults('graphics', {
			'width': 800,
			'height': 600
		})

	# build & return "root" widget
	def build(self):
		# initialize game basics
		self.bootstrap()
		self.initialize_game_dir()
		self.initialize_mod()
		self.initialize_map()
		self.initialize_manager_locator()
		# initialize L
		# initialize user interface
		self._build_user_interface()
		root_layout = L.WidgetManager.get_widget("root_layout")
		# start game loop and return root FloatLayout
		self._start_game_loop()
		return root_layout

	def on_start(self):
		print "Application started"

	# boot game core
	def bootstrap(self):
		L.InputManager = InputManager()
		L.GameLoopManager = GameLoopManager()
		L.WidgetManager = WidgetManager()

	# initialize game root directory
	def initialize_game_dir(self):
		game_root = os.path.abspath(__file__ + "/../../")
		L.RootDirectory = game_root
		FileManager.set_game_root(game_root)

	# initialize L manager holder
	def initialize_manager_locator(self):
		# set basic managers in L class
		# Manager initialization inside L holder class
		L.PlayerManager = PlayerManager()
		L.UnitManager = UnitManager()
		L.CityManager = CityManager()

	# load and set Mod to start
	def initialize_mod(self):
		L.ModManager = ModManager(mod_name = self.MOD_NAME)

	# load and set TileMap to start
	def initialize_map(self):
		L.MapManager = MapManager(map_name=self.MAP_NAME)
		tilemap = L.MapManager.load_map(self.MAP_NAME)
		L.TileMap = tilemap

	# make the root kivy Layout and register it in WidgetManager
	def _build_user_interface(self):
		# create root kivy Layout
		root_layout = FloatLayout(pos=(0,0), size=(800, 600))
		L.WidgetManager.register("root_layout", root_layout)
		# add MapWidget to root and WidgetManager
		mapwidget = MapWidget()
		bottombar = BottomBar()
		root_layout.add_widget(mapwidget)
		root_layout.add_widget(bottombar)
		L.WidgetManager.register("mapwidget", mapwidget)
		L.WidgetManager.register("bottombar", bottombar)
		return root_layout

	def _start_game_loop(self):
		# start loop & first turn
		L.GameLoopManager.run()
		L.PlayerManager.start_game()
