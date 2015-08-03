from core.entities.event import *
from core.lang.borg import Borg
from weakref import WeakKeyDictionary

class EventManager:
	_tag = "[EventManager] "
	listeners = WeakKeyDictionary()
	eventQueue= []

	@classmethod
	def register_listener(self, listener):
		self.listeners[listener] = 1

	@classmethod
	def unregister_listener( self, listener ):
		if listener in self.listeners:
			del self.listeners[listener]

	@classmethod
	def fire(self, event):
		if not isinstance(event, TickEvent):
			print(self._tag + "Message: " + event.name)
		for listener in list(self.listeners):
			listener.on_event(event)