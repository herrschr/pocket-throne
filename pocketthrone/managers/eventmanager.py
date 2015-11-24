from pocketthrone.entities.event import *
from weakref import WeakKeyDictionary

class EventManager:
	_tag = "[EventManager] "
	listeners = WeakKeyDictionary()
	eventQueue= []

	@classmethod
	def register_listener(self, listener, tag="untagged"):
		self.listeners[listener] = 1
		print(self._tag + "registered " + str(listener.__class__) + " in event queue.")

	@classmethod
	def unregister_listener( self, listener):
		if listener in self.listeners:
			print(self._tag + "unregistered " + str(listener.__class__) + " from event queue")
			del self.listeners[listener]

	@classmethod
	def fire(self, event):
		if not isinstance(event, TickEvent) and not isinstance(event, MouseMovedEvent):
			print(self._tag + "EVENT " + event.name)
		for listener in list(self.listeners):
			listener.on_event(event)