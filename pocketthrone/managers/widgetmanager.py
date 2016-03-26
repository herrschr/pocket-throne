__all__ = ('WidgetManager')
import string
from copy import deepcopy

from kivy.core.window import Window

from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetState, WidgetAction, GameState, CoordinateAxis
from pocketthrone.entities.tilemap import TileMap, GridTranslation
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.widgets.sidebar import SideBar, SideBarType
from pocketthrone.managers.pipe import L

class WidgetManager:
	WIDTH = 800
	HEIGHT = 600
	TILESIZE = 40

	root = None

	# engine properties
	_tag = "[WidgetManager] "
	_initialized = False
	has_sidebar = False

	# game-wide WidgetManager
	gamestate = GameState.STATE_INITIALIZING
	linked = {}
	dimens = {"x": 0, "y": 0}
	grid = {"width": 0, "height": 0}

	# scrolling related
	prev_scrolling = {"x": 0, "y": 0}
	scrolling = {"x": 0, "y": 0}
	scrolling_has_changed = False

	def __init__(self):
		# register in EventManager
		EventManager.register(self)
		# initialize screen & grid dimensions
		self.update_screen()
		# set GameState to LOADING
		self._initialized = True
		self.set_gamestate(GameState.STATE_LOADING)

	def update_screen(self):
		'''updates grid and screen dimension'''
		# add width & height to self.dimens
		self.dimens["width"] = self.WIDTH
		self.dimens["height"] = self.HEIGHT
		L.Screen = self.get_dimens()
		# add width & height to self.grid
		self.grid["width"] = int(self.WIDTH / self.TILESIZE)
		self.grid["height"] = int(self.HEIGHT / self.TILESIZE)
		L.Grid = self.get_grid()
		# print new size
		print(self._tag + "screen size is " + repr(self.dimens))
		print(self._tag + "grid size is " + repr(self.grid))

	def get_dimens(self):
		'''returns a copy of screen size as tuple'''
		return deepcopy(self.dimens)

	def set_gamestate(self, value):
		'''sets gamestate'''
		self.gamestate = value
		# fire GameStateChangedEvent
		ev_state_changed = GameStateChangedEvent(value)
		EventManager.fire(ev_state_changed)

	def get_gamestate(self):
		'''returns gamestate'''
		return self.gamestate

	def get_grid(self):
		'''returns this screens grid size'''
		return deepcopy(self.grid)

	def get_scrolling(self):
		'''returns scrolling offset'''
		return deepcopy(L.MapManager.scrolling)

	# TODO: remove
	def scroll(self, (plus_x, plus_y)):
		# self.scrolling["x"] = int(self.scrolling["x"]) + int(plus_x)
		# self.scrolling["y"] = int(self.scrolling["x"]) + int(plus_y)
		pass

	def to_grid_pos(self, (pos_x, pos_y)):
		'''translate a pixel position into the tile grid'''
		map_x = int(pos_x / 40)
		map_y = int(pos_y / 40)
		# invert y axis
		inv_y = L.Grid["height"] - map_y
		return (map_x, map_y)

	def to_relative_pos(self, translation):
		'''returns a relative position vector from given GridTranslation'''
		axis = grid_translation.axis
		value = grid_translation.value
		# initialize maximal values for dimensions
		max = {"x": L.Grid["width"], "y": L.Grid["height"]}
		# initialize pos
		if value < 0:
			value = max[axis] - value
		elif value == 0:
			value = 0
		elif value > 0:
			value = 0 + value
		# when translation is vertical
		if axis == CoordinateAxis.AXIS_Y:
			return (0, pos)
		# when translation is horizontal
		elif axis == CoordinateAxis.AXIS_X:
			return (pos, 0)

	def _to_grid_translation(self, axis=CoordinateAxis.AXIS_X, forwards=True, value=0):
		forwards = True
		axis = axis
		pos = {"x": 0, "y": 0}
		rel_pos = None
		max = {
			"x": self.get_grid()["width"],
			"y": self.get_grid()["height"]
		}
		value = value
		# check if counting starts backwards
		if value < 0:
			forwards = False
		# create & return relative coordinates
		translation = GridTranslation(axis=axis, value=value)
		return translation

	def to_gui_pos(self, (map_x, map_y), y_inv=True):
		'''returns a screen position for a grid position'''
		#gui_x = self.x + (map_x *40)
		gui_x = 0 + (map_x *40)
		gui_y = 0 + ((map_y +1) *40)
		# TODo remove fixed height
		inv_y = 600 - gui_y
		if y_inv:
			return (gui_x, inv_y)
		else:
			return (gui_x, gui_y)

	# returns a grid position considering the actual scrolling offset
	def to_scrolled_pos(self, (grid_x, grid_y)):
		'''returns a scrolled grid position'''
		scrolled_x = grid_x + int(L.MapManager.scrolling["x"])
		scrolled_y = grid_y + int(L.MapManager.scrolling["y"])
		return (scrolled_x, scrolled_y)

	def next_panel_id(self):
		'''returns a new unique panel id'''
		_id = self._last_panel_id + 1
		return _id

	def get_screen_size(self):
		'''returns the size of the game window in px'''
		return (Window.width, Window.height)

	def register(self, link, widget):
		'''registers widget under link'''
		# check if widget registration is valid
		if link == None or link == "untagged":
			print(self._tag + "ERROR widget registration aborted for " + link)
			return None
		# add widget link to self.linked
		self.linked[link] = widget
		# print & return widget
		print(self._tag + "registered link=" + link)
		return widget

	def get_widget(self, link):
		'''returns widget under link or None'''
		widget = None
		success = False
		# untagged widget -> loading unsuccessful
		if link == None or link == "untagged":
			success = False
		# widget is tagged -> load from self.linked dict
		else:
			widget = self.linked.get(link)
			# set success true when widget isn't None
			if widget != None:
				success = True
		# return widget under name link
		return widget

	def remove_widget(self, link):
		'''removes widget under link'''
		widget = self.get_widget(link)
		self.root.remove_widget(widget)

	def _remove_widget(self, widget):
		'''removes widget by class'''
		root = self.get_widget("root_layout")
		root.remove_widget(widget)

	def button_clicked(self, button):
		'''triggered when a button was clicked'''
		ev_button_clicked = ButtonTouchedEvent(button.link, button.action, widget=button, extra=button.extra)
		EventManager.fire(ev_button_clicked)

	def on_event(self, event):
		if isinstance(event, GameStartedEvent):
			self.gamestate = GameState.STATE_INGAME

		# clear BottomBar Labels on TileUnselectedEvent
		if isinstance(event, TileUnselectedEvent):
			# change labels
			self.get_widget("heading").set_text("")
			self.get_widget("details").set_text("")
			# get actionbutton; set action & state
			actionbutton = self.get_widget("actionbutton")
			actionbutton.set_action(WidgetAction.ACTION_NONE)
			actionbutton.set_state(WidgetState.STATE_DEFAULT)

		# show unit data in BottomBar on UnitSelectedEvent
		if isinstance(event, UnitSelectedEvent):
			heading = self.get_widget("heading")
			details = self.get_widget("details")
			heading.set_plaintext("Unit: " + event.unit.name)
			details.set_plaintext("HP: " + str(event.unit.hp) + " | MP: " + str(event.unit.mp))

		# show city data in BottomBar on CitySelectedEvent
		if isinstance(event, CitySelectedEvent):
			city = event.city
			# get production info text
			txt_prod_info = "nothing"
			if city.is_recruiting():
				txt_prod_info = str(city.name_production()) + " (" + str(city._recruition().get_duration()) + ")"
			# make text for heading and detail label
			txt_city_heading = city.name_size() + ": " + city.get_name()
			txt_city_details = "HP: " + str(city.get_hp()) + " | In Production: " + txt_prod_info
			# get labels & actionbutton
			heading = self.get_widget("heading")
			details = self.get_widget("details")
			actionbutton = self.get_widget("actionbutton")
			# change labels
			heading.set_text(txt_city_heading)
			details.set_text(txt_city_details)
			# set actionbutton state BUILD
			actionbutton.set_action(WidgetAction.ACTION_BUILD)
			# show sidebar
			sidebar = SideBar(SideBarType.RECRUIT)
			root = self.get_widget("root_layout")
			root.add_widget(sidebar)

		# handle Button clicks
		if isinstance(event, ButtonTouchedEvent):
			link = event.link
			action = event.action
			print(self._tag + "ButtonTouchedEvent link=" + link)
			if not action:
				print(self._tag + "NO ACTION; ABORTING")
			# BUILD
			if action == WidgetAction.ACTION_BUILD:
				# check if a City is selected
				selected_city = L.CityManager.get_selected_city()
				if not selected_city:
					return None

				# show recruitable units on it
				recruitable_units = L.CityManager.get_recruitable_units(selected_city)
				sidebar.show_recruitable_units(recruitable_units)

			# NEXT TURN
			if link == "nextturnbutton":
				L.PlayerManager.forward()

		# gamestate changes
		if isinstance(event, GameStateChangedEvent):
			# menu initialized
			if  event.state == GameState.STATE_MENU:
				pass
			# loading...
			elif event.state == GameState.STATE_LOADING:
				pass
			# ingame
			elif event.state == GameState.STATE_MAP:
				# update dimens & grid
				self.update_screen()

		if isinstance(event, KeyPressedEvent):
			if event.key == "spacebar":
				L.PlayerManager.forward()
