__all__ = ['GuiManager']
import string

from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window

from pocketthrone.entities.event import *
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.gui import *
from pocketthrone.gui.sidebar import SideBar
from pocketthrone.managers.locator import Locator

class GuiManager:
	# layouts
	_tag = "[GuiManager] "
	gamestate = GAMESTATE_MENU
	widgets_by_id = {}

	def __init__(self):
		EventManager.register_listener(self)
		self.set_gamestate(GAMESTATE_LOADING)

	# set gamestate
	def set_gamestate(self, value):
		self.gamestate = value
		# fire GameStateChangedEvent
		ev_state_changed = GameStateChangedEvent(value)
		EventManager.fire(ev_state_changed)

	# returns gamestate
	def get_gamestate(self):
		return self.gamestate

	# returns a new gui panel id
	def next_panel_id(self):
		self._last_panel_id += 1
		return self._last_panel_id

	# returns the screen size in px as tuple
	def get_screen_size(self):
		return (Window.width, Window.height)

	# register widget_id in GuiManager
	def register_widget(self, widget_id, widget):
		# check if widget registration is valid
		if string.strip(widget_id) == "untagged":
			print(self._tag + "ERROR widget registration aborted for " + string.strip(widget_id))
			return None
		self.widgets_by_id[string.strip(widget_id)] = widget
		print(self._tag + "registered widget_id=" + string.strip(widget_id))
		return widget

	# returns widget with string widget_id or None
	def get_widget(self, widget_id):
		widget = None
		stripped_id = widget_id.strip()
		success = False
		# filter untagged
		if stripped_id == "untagged":
			success = False
		try:
		# try to get from widget list
			widget = self.widgets_by_id[stripped_id]
			success = True
		finally:
			print(self._tag + "get widget _id=" + string.strip(widget_id) + "  2nd_acc=" + str(success) + " widget=" + repr(widget))
			return widget

	# removes widget entity from GuiManager
	def remove_widget(self, widget_id):
		widget = self.get_widget(widget_id)
		root.remove_widget(widget)

	# fire ButtonClickedEvent when a button is pressed
	def button_clicked(self, button):
		ev_button_clicked = GuiButtonClickedEvent(button.tag, button)
		EventManager.fire(ev_button_clicked)

	def on_event(self, event):
		if isinstance(event, GameStartedEvent):
			self.gamestate = GAMESTATE_INGAME
		# clear BottomBar Labels on TileUnselectedEvent
		if isinstance(event, TileUnselectedEvent):
			# change labels
			self.get_widget("heading").set_text("")
			self.get_widget("details").set_text("")
			# get actionbutton
			actionbutton = self.get_widget("actionbutton")
			actionbutton.set_button_state("DEFAULT")

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
				txt_prod_info = str(city.get_unit_in_production().name) + " (" + str(city.production_time) + ")"
			# make text for heading and detail label
			txt_city_heading = city.get_size_name() + ": " + city.get_name()
			txt_city_details = "HP: " + str(city.get_hp()) + " | In Production: " + txt_prod_info
			# get labels & actionbutton
			heading = self.get_widget("heading")
			details = self.get_widget("details")
			actionbutton = self.get_widget("actionbutton")
			# change labels
			heading.set_text(txt_city_heading)
			details.set_text(txt_city_details)
			# set actionbutton state BUILD
			actionbutton.set_button_state("BUILD")

		# handle Button clicks
		if isinstance(event, GuiButtonClickedEvent):
			print(self._tag + "GuiButtonClickedEvent widget_id=" + event.widget_id)
			# ACTION button
			if event.widget_id == "actionbutton":
				# BUILD action inside a city
				if event.button_state == "BUILD":
					selected_city = Locator.CITY_MGR.get_selected_city()
					# abort if no city is selected
					if not selected_city:
						return
					# add sidebar
					sidebar = SideBar()

					root = self.get_widget("root")
					root.add_widget(sidebar)
					# show recruitable units on it
					recruitable_units = Locator.CITY_MGR.get_recruitable_units(selected_city)
					sidebar.show_recruitable_units(recruitable_units)
		# gamestate changes
		if isinstance(event, GameStateChangedEvent):
			# menu initialized
			if  event.state == GAMESTATE_MENU:
				pass
			# loading...
			elif event.state == GAMESTATE_LOADING:
				pass
			# ingame
			else:
				pass