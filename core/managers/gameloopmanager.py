from core.entities.event import *
import sys

# GameLoopManager
# handles the gameloop instead of the main script before
class GameLoopManager:
	def __init__(self, eventmanager):
		# init eventmanager and keepGoing
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)
		self.keepGoing = 1

	# start the gameloop
	def run(self):
		# fire GameStartedEvent
		ev_game_started = GameStartedEvent()
		self._eventmgr.post(ev_game_started)
		while self.keepGoing:
			event = TickEvent()
			self._eventmgr.post(event)

	# stop the gameloop on QuitEvent
	def on_event(self, event):
		if isinstance(event, QuitEvent):
			#this will stop the while loop from running
			self.keepGoing = False
			sys.exit()