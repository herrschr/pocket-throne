__all__ = ('BottomBar')

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.graphics import *

from pocketthrone.managers.locator import Locator
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.gui.gamebutton import GameButton
from pocketthrone.gui.gamelabel import GameLabel
from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetState, WidgetAction

class BottomBar(BoxLayout):
	_tag = "[BottomBar] "
	_dirty = True

	def __init__(self, **kwargs):
		super(BottomBar, self).__init__(orientation="horizontal", size_hint=(1, .1), pos=(0,0))
		EventManager.register_listener(self)
		# auto-register in GuiManager
		Locator.GUI_MGR.register_widget("bottombar", self)

		# make GameButtons
		actionbutton = GameButton(size_hint=(.1, 1), widget_id="actionbutton", action=WidgetAction.ACTION_NONE)
		nextturnbutton = GameButton(size_hint=(.1, 1), widget_id="nextturnbutton", action=WidgetAction.ACTION_NEXTTURN)

		# make label widgets
		labels = BoxLayout(orientation="vertical", halign="left", valign="top", size_hint=(1, .75))
		heading = GameLabel(widget_id="heading", weight=1.4)
		details = GameLabel(widget_id="details", weight=1.0)
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
		heading_text = Locator.GUI_MGR.get_widget("heading").get_text()
		return heading_text

	def set_heading_text(self, value):
		heading_label = Locator.GUI_MGR.get_widget("heading").set_text(value)

	def get_details_text(self):
		details_text = Locator.GUI_MGR.get_widget("details").get_text()
		return details_text

	def set_details_text(self, value):
		Locator.GUI_MGR.get_widget("details").set_text(value)

	def set_actionbutton_state(self, value):
		actionbutton = Locator.GUI_MGR.get_widget("actionbutton")
		actionbutton.set_button_state(value)

	def get_actionbutton_state(self):
		actionbutton = Locator.GUI_MGR.get_widget("actionbutton")
		return actionbutton.get_button_state()

	def update_background(self):
		pass

	def on_event(self, event):
		if isinstance(event, TickEvent):
			self.update()