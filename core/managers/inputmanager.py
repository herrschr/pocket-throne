from kivy.core.window import Window
from core.entities.event import *
from core.managers.eventmanager import EventManager

class InputManager:
	_last_mousepos = None

	def __init__(self):
		EventManager.register_listener(self)

	def on_event(self, event):
		if isinstance(event, TickEvent):
			kivy_mousepos = Window.mouse_pos
			inv_mouse_y = Window.height - kivy_mousepos[1]
			mousepos = (kivy_mousepos[0], inv_mouse_y)
			if self._last_mousepos != mousepos:
				# fire MouseMovedEvent
				ev_mouse_moved = MouseMovedEvent(mousepos)
				EventManager.fire(ev_mouse_moved)
				# update last mouse position
				self._last_mousepos = mousepos
