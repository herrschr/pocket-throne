from pocketthrone.entities.event import *
import sys
from pocketthrone.managers.eventmanager import EventManager
from kivy.clock import Clock

# GameLoopManager
# handles the gameloop instead of the main script before
class GameLoopManager:
	def __init__(self):
		# init eventmanager and keepGoing
		EventManager.register(self)
		self.keepGoing = True

	def run(self):
		'''starts the game loop'''
		# fire GameStartedEvent
		ev_game_started = GameStartedEvent()
		EventManager.fire(ev_game_started)
		# schedule tickevent with 60 fps
		Clock.schedule_interval(self.tick, 1/60)

	def tick(self, dt):
		'''fires next tick'''
		event = TickEvent()
		EventManager.fire(event)

	# stop the gameloop on QuitEvent
	def on_event(self, event):
		if isinstance(event, QuitEvent):
			#this will stop the while loop from running
			self.keepGoing = False
			sys.exit()
