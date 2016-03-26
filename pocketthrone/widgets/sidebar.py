__all__ = ('SideBar')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetAction, WidgetState, Enum

from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.managers.pipe import L

class SideBarType(Enum):
	RECRUIT = "recruit"
	CONSTRUCT = "construct"

# kivy widget implementation of the SideBar, used for recruiting, build & menu buttons
# please create it first and then call a show_* method
class SideBar(BoxLayout):
	_tag = "[SideBar] "

	rows = []
	sidebar_type = None

	is_initialized = False

	# initialize with BoxLayout parameters
	def __init__(self, sidebar_type):
		# make vertical BoxLayout
		super(SideBar, self).__init__(orientation="vertical", padding=4, size_hint=(.3, .8), pos=(0, 100))
		# register in EventManager and WidgetManager
		EventManager.register(self)
		L.WidgetManager.register("sidebar", self)
		# load unit or building list
		self.sidebar_type = sidebar_type
		# show recruitable units
		if sidebar_type == SideBarType.RECRUIT:
			self.show_recruitable()
		# show constructable buildings
		elif sidebar_type == SideBarType.CONSTRUCT:
			self.show_constructable()
		else:
			print(self._tag + "ABORT; type " + str(sidebar_type) + " isn't valid.")

	def show_recruitable(self):
		'''shows recruitable units'''
		selected_city = L.CityManager.get_selected_city()
		# abort when no city is selected
		if not selected_city:
			print(self._tag + "ABORT; no city is selected")
			return
		# load recruitable units
		blueprints = L.CityManager.get_recruitable_units(selected_city)
		if len(blueprints) == 0:
			print(self._tag + "ABORT; no units received")
			return
		for blueprint in blueprints:
			unit_name = "  " + blueprint.get_name()
			unit_basename = blueprint.get_basename()
			image_src = "img/" + blueprint.get_image_path() + ".png"
			# make outter layout
			outter = BoxLayout(orientation="horizontal", size_hint=(1, None), size=(300, 60))
			# make image
			image = Image(source=image_src, size=(60, 60), on_touch_down=self.option_selected)
			image.extra = unit_basename
			# make label
			label = Label(text=unit_name, font_size="20dp", halign="left", on_touch_down=self.option_selected, size=(200, 60), valign="middle", color=[0,0,0,1])
			label.text_size = label.size
			label.extra = unit_basename
			# add both to layout
			outter.add_widget(image)
			outter.add_widget(label)
			# add layout to SideBar
			self.add_widget(outter)
		self.is_initialized = True

	def show_constructable(self):
		pass

	# TODO replace with add_row
	def add_widget(self, widget):
		'''# add a widget to SideBar and the buttons list'''
		super(SideBar, self).add_widget(widget)
		widget.bind(on_press=self.option_selected)
		self.rows.append(widget)

	def add_rows(self):
		pass

	def remove_self(self):
		'''method to destroy this SideBar widget'''
		L.WidgetManager.get_widget("root_layout").remove_widget(self)

	def option_selected(self, widget, touch):
		'''triggered when an list item was selected'''
		if widget.collide_point(*touch.pos):
			print(self._tag + "clicked " + widget.extra)
			if self.sidebar_type == SideBarType.RECRUIT:
				# load blueprint & selected city
				unit_type = widget.extra
				blueprint = L.UnitManager.get_blueprint(unit_type)
				selected_city = L.CityManager.get_selected_city()
				# finish recruitation
				L.CityManager.recruit_unit(selected_city, blueprint)
		# destroy sidebar
		self.remove_self()

	def on_event(self, event):
		# destroy SideBar on map click
		if isinstance(event, TileUnselectedEvent):
			self.remove_self()
