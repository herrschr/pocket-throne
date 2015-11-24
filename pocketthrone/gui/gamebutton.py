__all__ = ('GameButton', 'ButtonState')

import string

from kivy.properties import *
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel

from pocketthrone.managers.locator import Locator
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetState, WidgetAction

class GameButton(Image):
	# widget constants
	ID_DEFAULT = "NO_ID"
	EXTRA_DEFAULT = "default"

	_tag = "[GameButton] "
	state = WidgetState(initial=WidgetState.STATE_DEFAULT)
	action = WidgetAction(initial=WidgetAction.ACTION_NONE)
	extra = "NOEXTRA"

	widget_id = "untagged"
	label = None
	_dirty = True
	text = ""

	def __init__(self, widget_id=ID_DEFAULT, action=WidgetAction.ACTION_NONE ,**kwargs):
		super(GameButton, self).__init__(**kwargs)
		EventManager.register_listener(self)
		Locator.GUI_MGR.register_widget(widget_id, self)
		# set optional properties
		self.source = FileManager.image_path() + "none.png"
		self.widget_id = widget_id
		self.button_tag = string.upper(widget_id)
		self.extra = extra
		print(self._tag + "init start source=" + self.source)

	def update(self):
		if self._dirty == True:
			self.update_source()
			self.update_label()
		self._dirty = False

	def on_touch_down(self, touch):
		if touch.button == "left":
			# translate y pos (0|0 is on top left of the window)
			touch_inv_y = Window.height - touch.y
			# fire MouseClickedEvent
			ev_button_clicked = GuiButtonClickedEvent(self.widget_id, self.get_state(), widget=self)
			EventManager.fire(ev_button_clicked)

	# set image root related path as background icon
	def set_source(self, icon_source):
		self.source = FileManager.image_path() + icon_source
		self.update()
		print(self._tag + "button icon is " + icon_source)

	# set the ActionButtons state ("sub-tag")
	def set_state(self, state):
		self.state = state
		self.update()
		print(self._tag + "button state is now "+ repr(state))

	# get the ActionButtons GameButtonState ("sub-tag")
	def get_state(self):
		return self.state

	def set_action(self, value):
		self.action = value

	def get_action(self):
		return self.action

	# automatically update background iconresource
	def update_source(self):
		background_src = FileManager.image_path() + self.widget_id + "_bg_" + self.get_action().get() +  ".png"
		print(self._tag + "background image is " + background_src)
		texture = Image(src=background_src).texture
		self.source = background_src
		with self.canvas:
			Rectangle(texture=texture, size=(self.width, self.height))

	def get_extra(self):
		return self.extra

	def set_extra(self, value):
		self.extra = value

	# update the label text
	def update_label(self):
		if self.label == None:
			# create new label
			label = CoreLabel(text=self.get_text(), font_size=12, color=(0, 0, 1))
			label.refresh();
			self.label = label
		labeltexture= self.label.texture
		labelsize = list(labeltexture.size)
		# self.canvas.add(Rectangle(texture=labeltexture, size=(self.width, self.height)))

	def set_text(self, value):
		self.text = value
		self.update()

	def get_text(self):
		return self.text

	# get absolute path of this ActionButtons background icon
	def get_source(self):
		return self.source

	# trigger a widget full redraw
	def trigger_redraw(self):
		self._dirty = True

	def on_event(self, event):
		# redraw the map when required each TickEvent
		if isinstance(event, TickEvent):
			self.update()


