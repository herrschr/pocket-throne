from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

from core.entities.event import *

from core.managers.eventmanager import EventManager
from core.managers.locator import Locator

class SideBar(BoxLayout):
	buttons = []

	# initilaize with BoxLayout parameters
	def __init__(self, **kwargs):
		super(SideBar, self).__init__(orientation="vertical", padding=10, size_hint=(.2, .8), pos=(0, 100))
		EventManager.register_listener(self)

	# add a widget to SideBar and the buttons list
	def add_widget(self, widget):
		super(SideBar, self).add_widget(widget)
		self.buttons.append(widget)

	# Show recruitable units when a city is selected
	def show_recruitable_units(self, recruitable):
		for blueprint in recruitable:
			text = blueprint.get_name()
			tag = "BUILD-" + blueprint._basename.upper()
			buildunitbutton = Button(text=text, size_hint=(1, None), size=(100, 40), on_press=Locator.GUI_MGR.button_clicked)
			buildunitbutton.tag = tag
			self.add_widget(buildunitbutton)

	def remove_self(self):
		self.parent.remove_widget(self)

	def on_event(self, event):
		if isinstance(event, GuiButtonClickedEvent):
			if event.button.parent == self:
				self.remove_self()