from core.lib.posix.pygame_sdl2.sprite import Sprite
from core.entities.event import *

class Widget(Sprite):
	WIDGET_ALIGN_TOP = 1
	WIDGET_ALIGN_RIGHT = 2
	WIDGET_ALIGN_BOTTOM = 3
	WIDGET_ALIGN_LEFT = 4
	WIDGET_ALIGN_CENTER = 5

	def __init__(self, eventmanager):
		# init parent class (Pygame sprite)
		Sprite.__init__(self)
		# register in eventmanager
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)
		# not focused; to be redrawn
		self._focused = False
		self._redraw = True

	# set focus and redraw
	def set_focus(self, focused):
		self._focused = focused
		self._redraw = True

	def remove(self):
		Sprite.kill(self)

	def on_event(self, event):
		if isinstance(event, GuiWidgetFocusedEvent):
			# on focus
			if event.widget == self:
				self.set_focus(True)
			# unfocus widget when another is selected as focused
			elif self.focused:
				self.set_focus(False)
		if isinstance(event, GuiWidgetUnfocusedEvent):
			# unfocus widget on GuiWidgetUnfocusedEvent
			if self.focused:
				self.set_focus(False)