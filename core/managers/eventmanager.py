from core.entities.event import *

class EventManager:
	# this object is responsible for coordinating most communication
	def __init__(self):
		from weakref import WeakKeyDictionary
		self.listeners = WeakKeyDictionary()
		self.eventQueue= []

	def register_listener(self, listener):
		self.listeners[listener] = 1

	def unregister_listener( self, listener ):
		if listener in self.listeners:
			del self.listeners[listener]

	def post(self, event ):
		if not isinstance(event, TickEvent):
			print( "EventManager: Message: " + event.name )
		for listener in list(self.listeners):
			listener.on_event(event)