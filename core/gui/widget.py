from pygame_sdl2.sprite import Sprite
from core.entities.event import *

class Widget:
	_id = -1
	_pos_in_panel = -1
	WIDGET_ALIGN_TOP = 1
	WIDGET_ALIGN_RIGHT = 2
	WIDGET_ALIGN_BOTTOM = 3
	WIDGET_ALIGN_LEFT = 4
	WIDGET_ALIGN_CENTER = 5

	def __init__(self, eventmanager):
		# init parent class (Pygame sprite)
		# Sprite.__init__(self)
		# register in eventmanager
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)
		# not focused; to be redrawn
		self._focused = False
		self.dirty = True
		# layout properties
		self.layout_override = False
		self.left = None
		self.top = None
		self.width = None
		self.height = None
		# no parent panel yet
		self.parent = None

	# trigger a widget redraw of this widget the parent panel
	def trigger_redraw(self):
		# set dirty flag in widget
		self.dirty = True
		# update widget's parent panel
		if self.parent != None:
			# fire GuiPanelUpdatedEvent
			ev_panel_updated = GuiPanelUpdatedEvent(self.parent)
			self._eventmgr.fire(ev_panel_updated)

	# set focus and redraw
	def set_focus(self, focused):
		self._focused = focused
		self.dirty = True

	# base method for a widget
	def update(self):
		pass

	# get panel position and dimensions as tuple
	def get_layout(self):
		return (self.left, self.top, self.width, self.height)

	# set full layout (x,y,width,height)
	def set_layout(self, (left, top, width, height)):
		if left:
			self.left = left
		if top:
			self.top = top
		if width:
			self.width = width
		if height:
			self.height = height

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