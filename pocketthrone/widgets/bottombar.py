__all__ = ('BottomBar')

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.graphics import *

from pocketthrone.managers.pipe import L
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.widgets.gamebutton import GameButton
from pocketthrone.widgets.gamelabel import GameLabel
from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetState, WidgetAction

class BottomBar(BoxLayout):
	_tag = "[BottomBar] "
	_dirty = True

	def __init__(self, **kwargs):
		super(BottomBar, self).__init__(orientation="horizontal", size_hint=(1, .1), pos=(0,0))
		EventManager.register(self)

		# make GameButtons
		actionbutton = GameButton(size_hint=(.1, 1), link="actionbutton")
		actionbutton.set_source("actionbutton_bg_default.png")
		nextturnbutton = GameButton(size_hint=(.1, 1), link="nextturnbutton")

		# make label widgets
		labels = BoxLayout(orientation="vertical", halign="left", valign="top", size_hint=(1, .75))
		heading = GameLabel(link="heading", weight=1.4)
		details = GameLabel(link="details", weight=1.0)
		labels.add_widget(heading)
		labels.add_widget(details)

		# add all to BottomBars background
		self.add_widget(actionbutton)
		self.add_widget(labels)
		self.add_widget(nextturnbutton)

	def trigger_redraw(self):
		self._dirty = True

	# add a widget to SideBar and the buttons list
	def add_widget(self, widget):
		print(self._tag + "add widget " + repr(widget))
		super(BottomBar, self).add_widget(widget)

	# method to destroy this BottomBar widget
	def remove_self(self):
		self.parent.remove_widget(self)

	def update(self):
		if self._dirty:
			self.update_background()
		self._dirty = False

	def get_heading_text(self):
		heading_text = L.WidgetManager.get_widget("heading").get_text()
		return heading_text

	def set_heading_text(self, value):
		heading_label = L.WidgetManager.get_widget("heading").set_text(value)

	def get_details_text(self):
		details_text = L.WidgetManager.get_widget("details").get_text()
		return details_text

	def set_details_text(self, value):
		L.WidgetManager.get_widget("details").set_text(value)

	def set_actionbutton_state(self, value):
		actionbutton = L.WidgetManager.get_widget("actionbutton")
		actionbutton.set_button_state(value)

	def get_actionbutton_state(self):
		actionbutton = L.WidgetManager.get_widget("actionbutton")
		return actionbutton.get_button_state()

	def update_background(self):
		pass

	def on_event(self, event):
		if isinstance(event, TickEvent):
			self.update()
