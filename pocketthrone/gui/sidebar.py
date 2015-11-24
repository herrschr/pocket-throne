__all__ = ('SideBar')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetAction, WidgetState

from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.managers.locator import Locator

# kivy widget implementation of the SideBar, used for recruiting, build & menu buttons
# please create it forst and then call a show_* method
class SideBar(BoxLayout):
	_tag = "[BoxLayout] "
	buttons = []

	# initialize with BoxLayout parameters
	def __init__(self, **kwargs):
		super(SideBar, self).__init__(orientation="vertical", padding=4, size_hint=(.2, .8), pos=(0, 100))
		EventManager.register_listener(self)
		Locator.GUI_MGR.register_widget("sidebar", self)

	# add a widget to SideBar and the buttons list
	def add_widget(self, widget):
		super(SideBar, self).add_widget(widget)
		self.buttons.append(widget)

	# show recruitable units in this sidebar
	def show_recruitable_units(self, recruitable):
		for blueprint in recruitable:
			# show english unit name; set unit type as button tag
			name = blueprint.get_name()
			basename = blueprint._basename
			tag = "build-" + blueprint._basename.upper()
			# create a button for each unit and add it to sidebar
			buildunitbutton = Button(widget_id=build + basename + "button", text=text, size_hint=(1, None), size=(100, 30), on_press=Locator.GUI_MGR.button_clicked)
			buildunitbutton.action = WidgetAction.ACTION_BUILD
			buildbutton.extra = basename
			# add widget to sidebar
			self.add_widget(buildunitbutton)

	# method to destroy this SideBar widget
	def remove_self(self):
		self.parent.remove_widget(self)

	def on_event(self, event):
		# when a button is clicked -> destroy the sidebar (dialog style)
		if isinstance(event, GuiButtonClickedEvent):
			print(self._tag + "sidebar remove...")
			if event.button.parent == self:
				self.remove_self()