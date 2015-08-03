from kivy.uix.relativelayout import RelativeLayout
from core.entities.event import *
from core.managers.eventmanager import EventManager
from core.gui import *
from core.managers.locator import Locator

class GuiManager:
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
			# clear SideBar
			self.sidebar.clear_widgets()

		# show unit data in BottomBar on UnitSelectedEvent
		if isinstance(event, UnitSelectedEvent):
			self.bottombar.set_heading_text("Unit: " + event.unit.name)
			self.bottombar.set_details_text("HP: " + str(event.unit.hp) + " | MP: " + str(event.unit.mp))

		# show city data in BottomBar on CitySelectedEvent
		if isinstance(event, CitySelectedEvent):
			city = event.city
			prod_info = "nothing"
			if city.is_recruiting():
				prod_info = str(city.get_unit_in_production().name) + " (" + str(city.production_time) + ")"
			self.bottombar.set_heading_text(city.get_size_name() + ": " + city.get_name())
			self.bottombar.set_details_text("HP: " + str(city.get_hp()) + " | In Production: " + prod_info)

		# handle Button clicks
		if isinstance(event, GuiButtonClickedEvent):
			# ACTION button
			if event.button_tag == "ACTION":
				selected_city = Locator.CITY_MGR.get_selected_city
				# in city? show recruitable unit buttons
				if selected_city:
					recruitable_units = Locator.CITY_MGR.get_recruitable_units(selected_city)
					self.sidebar.show_recruitable_units(recruitable_units)