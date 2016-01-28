__all__ = ('SideBar')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetAction, WidgetState

from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.managers.locator import L

# kivy widget implementation of the SideBar, used for recruiting, build & menu buttons
# please create it first and then call a show_* method
class SideBar(BoxLayout):
	_tag = "[SideBar] "
	buttons = []

	is_initialized = False

	# initialize with BoxLayout parameters
	def __init__(self, **kwargs):
		super(SideBar, self).__init__(orientation="vertical", padding=4, size_hint=(.2, .8), pos=(0, 100))
		EventManager.register(self)
		L.WidgetManager.register("sidebar", self)
		self.is_initialized = True

	# add a widget to SideBar and the buttons list
	def add_widget(self, widget):
		super(SideBar, self).add_widget(widget)
		self.buttons.append(widget)

	# show recruitable units in this sidebar
	def show_recruitable_units(self, recruitable):
		# abort when SideBar is not initialized
		if not self.is_initialized:
			print(self._tag + " SideBar is not initialized; aborting SHOW RECRUITABLE UNITS")
		for blueprint in recruitable:
			# show english unit name; set unit type as button tag
			name = blueprint.get_name()
			basename = blueprint.basename
			link = "build-" + blueprint.basename.upper()
			# create a button for each unit and add it to sidebar
			buildunitbutton = Button(link=build + basename + "button", text=text, size_hint=(1, None), size=(100, 30))
			buildunitbutton.action = WidgetAction.ACTION_BUILD
			buildbutton.extra = basename
			# add widget to sidebar
			print(self._tag + "added button link=" + link)
			self.add_widget(buildunitbutton)

	def show_notifications(self):
		if not self.is_initialized:
			print(self._tag + " SideBar is not initialized; aborting SHOW RECRUITABLE UNITS")


	# method to destroy this SideBar widget
	def remove_self(self):
		self.parent.remove_widget(self)

	def on_event(self, event):
		# when a button is clicked -> destroy the sidebar (dialog style)
		if isinstance(event, ButtonTouchedEvent):
			print(self._tag + "sidebar remove...")
			if event.button.parent == self:
				self.remove_self()