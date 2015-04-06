from core.entities.event import *

class GameLoopManager:
	def __init__(self, eventmanager):
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)

		self.keepGoing = 1

	def run(self):
		while self.keepGoing:
			event = TickEvent()
			self._eventmgr.post(event)

	def on_event(self, event):
		if isinstance(event, QuitEvent):
			#this will stop the while loop from running
			self.keepGoing = False