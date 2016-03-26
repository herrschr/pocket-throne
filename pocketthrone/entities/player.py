from pocketthrone.entities.notification import Notification
from pocketthrone.entities.fraction import Fraction

class Player(object):
	def __init__(self):
		# engine properties
		self.num = -1
		# static player properties
		self.name = "Anonymous"
		self.color = (255, 0, 0)
		self._fraction_name = None
		self.fraction = None
		self.hero = None
		# changable player properties
		self.gold = 0
		# player properties for statistics
		self.killed_units = 0
		self.army_size = 0
		self.biggest_army_size = 0
		# recently selected entity position
		self.recently_selected = None
		# notifications
		self.notifications = []

	def __repr__(self):
		'''returns an xml like representation of this player'''
		return "<Player num=" + str(self.num) + " name=" + self.name + " gold=" + str(self.gold) + " fraction=" + repr(self.fraction) + ">"

	def get_number(self):
		'''returns the player number'''
		return self.num

	def get_name(self):
		'''returns the name of this player'''
		return self.name

	def get_color(self):
		'''returns the RGB color tuple of this player'''
		return self.color

	def get_fraction(self):
		'''returns the fraction entity of this player'''
		return self.fraction

	def get_gold(self):
		'''returns the gold treasure of this player'''
		return self.gold

	def gain_gold(self, amount):
		''''increase gold of this player by amount'''
		self.gold += amount

	def reduce_gold(self, gold_costs):
		'''decrease gold of this player by gold_costs'''
		self.gold -= gold_costs

	def add_notification(self, noti):
		'''adds an notification for next turn'''
		self.notifications.append(noti)

	def get_notifications(self):
		'''returns list of actual notifications'''
		return self.notifications

	def clear_notifications(self):
		'''removes any notification'''
		self.notifications = []
