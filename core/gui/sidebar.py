from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

from core.entities.event import *

from core.managers.eventmanager import EventManager
from core.managers.locator import Locator

# kivy widget implementation of the SideBar, used for recruiting, build & menu buttons
# please create it forst and then call a show_* method
class SideBar(BoxLayout):
	buttons = []

	# initialize with BoxLayout parameters
	def __init__(self, **kwargs):
		super(SideBar, self).__init__(orientation="vertical", padding=4, size_hint=(.2, .8), pos=(0, 100))
		EventManager.register_listener(self)

	# add a widget to SideBar and the buttons list
	def add_widget(self, widget):
		super(SideBar, self).add_widget(widget)
		self.buttons.append(widget)

	# show recruitable units in this sidebar
	def show_recruitable_units(self, recruitable):
		for blueprint in recruitable:
			# show english unit name; set unit type as button tag
			text = blueprint.get_name()
			tag = "BUILD-" + blueprint._basename.upper()
			# create a button for each unit and add it to sidebar
			buildunitbutton = Button(text=text, size_hint=(1, None), size=(100, 30), on_press=Locator.GUI_MGR.button_clicked)
			buildunitbutton.tag = tag
			self.add_widget(buildunitbutton)

	# method to destroy this SideBar widget
	def remove_self(self):
		self.parent.remove_widget(self)

	def on_event(self, event):
		# when a button is clicked -> destroy the sidebar (dialog style)
		if isinstance(event, GuiButtonClickedEvent):
			if event.button.parent == self:
				self.remove_self()