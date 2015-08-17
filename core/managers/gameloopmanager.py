from core.entities.event import *
import sys
from core.managers.eventmanager import EventManager
from kivy.clock import Clock

# GameLoopManager
# handles the gameloop instead of the main script before
class GameLoopManager:
	def __init__(self):
		# init eventmanager and keepGoing
		EventManager.register_listener(self)
		self.keepGoing = True

	# start the gameloop
	def run(self):
		# fire GameStartedEvent
		ev_game_started = GameStartedEvent()
		EventManager.fire(ev_game_started)
		# schedule tickevent with 40 fps
		Clock.schedule_interval(self.tick, 1/60)

	# fire a single TickEvent
	def tick(self, dt):
		event = TickEvent()
		EventManager.fire(event)

	# stop the gameloop on QuitEvent
	def on_event(self, event):
		if isinstance(event, QuitEvent):
			#this will stop the while loop from running
			self.keepGoing = False
			sys.exit()