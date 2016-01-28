__all__ = ('GameButton')

import string

from kivy.properties import *
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel

from pocketthrone.managers.locator import L
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.eventmanager import EventManager

from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetState, WidgetAction

class GameButton(Image):
	# widget constants
	ID_DEFAULT = "NO_ID"

	_tag = "[GameButton] "

	# widget state (DEFAULT, PRESSED, DISABLED, INVALID, INVISIBLE)
	state = WidgetState(initial=WidgetState.STATE_DEFAULT)
	# widget action (NONE, ATTACK, MOVE, BUILD, NEXTTURN)
	action = WidgetAction(initial=WidgetAction.ACTION_NONE)
	extra = None

	link = None
	label = None
	text = ""
	_corelabel = None

	_dirty = True

	def __init__(self, link=None, state=state,  action=action, extra=extra ,**kwargs):
		super(GameButton, self).__init__(**kwargs)
		EventManager.register(self)
		L.WidgetManager.register(link, self)
		# set optional properties
		image_dir = L.RootDirectory + "/img/"
		self.source = image_dir + str(link) + "_bg_" + str(action) + ".png"
		self.link = link
		self.button_tag = string.upper(link)
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
			ev_button_clicked = ButtonTouchedEvent(self.link, state=self.get_state(), action=self.get_action(), extra=self.get_extra())
			EventManager.fire(ev_button_clicked)

	# set image root related path as background icon
	def set_source(self, icon_source):
		self.source = L.RootDirectory + "img/" + icon_source
		self.update()
		print(self._tag + "button icon is " + icon_source)

	# set the widgets identifier for WidgetManager and click handling
	# TODO: remove link

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
		background_src = L.RootDirectory + "/img/" + self.link + "_bg_" + str(self.get_action()).lower() +  ".png"
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
