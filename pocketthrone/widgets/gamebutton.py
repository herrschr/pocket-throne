__all__ = ('GameButton')

import string

from kivy.properties import *
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel

from pocketthrone.managers.pipe import L
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.eventmanager import EventManager

from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetState, WidgetAction

class GameButton(Image):
	# widget constants
	ID_DEFAULT = "NO_ID"

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
	_tag = "[GameButton] "

	def __init__(self, link=None, state=state,  action=action, extra=extra ,**kwargs):
		super(GameButton, self).__init__(**kwargs)
		self.link = link
		EventManager.register(self)
		L.WidgetManager.register(link, self)
		# set optional properties
		self.button_tag = string.upper(link)
		self.extra = extra
		self.update()

	def update(self):
		'''update text and background image when neccessary'''
		if self._dirty == True:
			self.update_source()
			self.update_label()
		self._dirty = False

	def on_touch_down(self, touch):
		'''triggerd when button was pressed'''
		# check if touch collides with button
		if self.collide_point(*touch.pos):
			if touch.button == "left":
				# translate y pos (0|0 is on top left of the window)
				touch_inv_y = Window.height - touch.y
				# fire MouseClickedEvent
				ev_button_clicked = ButtonTouchedEvent(self.link, state=self.get_state(), action=self.get_action(), extra=self.get_extra())
				EventManager.fire(ev_button_clicked)

	def set_source(self, icon_source):
		'''set image root related path as background icon'''
		self.source = L.RootDirectory + "/img/" + icon_source
		self.update_source()

	def set_state(self, state):
		'''sets the ActionButtons state ("sub-tag")'''
		self.state = state
		self.update()
		print(self._tag + "button state is now "+ repr(state))

	def get_state(self):
		'''returns ActionButtons GameButtonState ("sub-tag")'''
		return self.state

	def set_action(self, value):
		'''sets buttons action (what it does)'''
		self.action = value
		self.update()

	def get_action(self):
		'''returns buttons action (what it does)'''
		return self.action

	def update_source(self):
		'''update buttons background resource'''
		image_dir = L.RootDirectory + "/img/"
		action_str = str(self.get_action()).lower()
		# background image name is <link>_bg_<action>.png
		background_src = image_dir + self.link + "_bg_" + action_str +  ".png"
		self.source = background_src
		# print icon image path
		print(self._tag + "background image is " + background_src + " for " + str(self.link))

	def get_extra(self):
		'''returns buttons extra information'''
		return self.extra

	def set_extra(self, value):
		'''sets buttons extra information'''
		self.extra = value

	def update_label(self):
		'''update buttons text'''
		if self.label == None:
			# create new label
			label = CoreLabel(text=self.get_text(), font_size=12, color=(0, 0, 1))
			label.refresh();
			self.label = label
		labeltexture= self.label.texture
		labelsize = list(labeltexture.size)
		# self.canvas.add(Rectangle(texture=labeltexture, size=(self.width, self.height)))

	def set_text(self, value):
		'''sets buttons text'''
		self.text = value
		self.update()

	def get_text(self):
		'''returns buttons text'''
		return self.text

	def get_source(self):
		'''returns absolute path of this ActionButtons background icon'''
		return self.source

	def trigger_redraw(self):
		'''trigger a widget full redraw'''
		self._dirty = True

	def on_event(self, event):
		# redraw the map when required each TickEvent
		if isinstance(event, TickEvent):
			# self.update()
			pass
