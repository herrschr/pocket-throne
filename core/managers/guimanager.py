from kivy.uix.relativelayout import RelativeLayout

from core.entities.event import *
from core.managers.eventmanager import EventManager
from core.gui import *
from core.gui.sidebar import SideBar
from core.managers.locator import Locator

class GuiManager:
	# layouts
	root = None
	mapwidget = None
	bottombar = None
	sidebar = None

	def __init__(self):
		EventManager.register_listener(self)
		self.gamestate = GAMESTATE_LOADING

	# returns a new gui panel id
	def next_panel_id(self):
		self._last_panel_id += 1
		return self._last_panel_id

	def remove_widget(self, widget):
		self.root.remove_widget(widget)

	# fire ButtonClickedEvent when a button is pressed
	def button_clicked(self, button):
		ev_button_clicked = GuiButtonClickedEvent(button.tag, button)
		EventManager.fire(ev_button_clicked)

	def on_event(self, event):
		# clear BottomBar Labels on TileUnselectedEvent
		if isinstance(event, TileUnselectedEvent):
			# clear BottomBar labels
			self.bottombar.set_heading_text("")
			self.bottombar.set_details_text("")
			self.bottombar.set_action("ACTION")

		# show unit data in BottomBar on UnitSelectedEvent
		if isinstance(event, UnitSelectedEvent):
			self.bottombar.set_heading_text("Unit: " + event.unit.name)
			self.bottombar.set_details_text("HP: " + str(event.unit.hp) + " | MP: " + str(event.unit.mp))

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
			# set BottomBar label & actionbutton texts
			self.bottombar.set_heading_text(txt_city_heading)
			self.bottombar.set_details_text(txt_city_details)
			self.bottombar.set_action("BUILD")

		# handle Button clicks
		if isinstance(event, GuiButtonClickedEvent):
			# ACTION button
			if event.button_tag == "ACTION":
				# BUILD action inside a city
				if self.bottombar.get_action() == "BUILD":
					selected_city = Locator.CITY_MGR.get_selected_city()
					# abort if no city is selected
					if not selected_city:
						return
					# add sidebar
					print("sidebar??")
					self.sidebar = SideBar()
					self.root.add_widget(self.sidebar)
					# show recruitable units on it
					recruitable_units = Locator.CITY_MGR.get_recruitable_units(selected_city)
					self.sidebar.show_recruitable_units(recruitable_units)