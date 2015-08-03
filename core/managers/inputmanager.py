from core.entities.event import *
from core.managers.eventmanager import EventManager

class InputManager:
	def __init__(self):
		EventManager.register_listener(self)

	def on_event(self, event):
		pass