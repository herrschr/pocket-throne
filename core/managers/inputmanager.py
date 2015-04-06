from core.lib.posix.pygame_sdl2 import *
from core.entities.event import *

# handles pygame events and translate them to corresponding EventManager events
class InputManager:
	def __init__(self, eventmanager):
		self._eventmgr = eventmanager
		self._eventmgr.register_listener( self )

	def on_event(self, event):
		if isinstance(event, TickEvent):
			#Handle Input Events
			for event in pygame_sdl2.event.get():
				response_event = None
				# on pygame.QUIT event
				if event.type == QUIT:
					response_event = QuitEvent()
				# on ESC
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					response_event = QuitEvent()
				# on mouse click
				elif event.type == MOUSEBUTTONDOWN:
					gui_pos = pygame_sdl2.mouse.get_pos()
					response_event = MouseClickedEvent(gui_pos)
				# post corresonding EventManager event
				if response_event != None:
					self._eventmgr.post(response_event)