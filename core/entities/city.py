from building import Building
from core.entities.unit import Unit
from core.entities.event import *
from random import randrange

from core.managers.eventmanager import EventManager

class City:
	# static city vars, defaults
	_id = -1
	name = ""
	name_de = ""
	image_path = None
	json_path = None
	size = "1x1"

	is_undestroyable = False
	is_owned_by_nature = False

	has_player_max = False
	has_map_max = False
	max_per_player = -1
	may_per_map = -1

	# changeable building vars
	playerId = -1
	city_size = 1
	hp = -1
	pos_x = -1
	pos_y = -1
	buildings = []

	production = []
	production_time = -1

	def __init__(self):
		# register as listener in EventManager
		EventManager.register_listener(self)
		# set name & hp
		self.hp = 30
		self.name = self.get_random_name()

	# generates a random name for the city
	def get_random_name(self):
		prefixes = ["Iron", "Green", "Wood", "Dragon", "Dried",  "Old", "New", "Saint", "Death"]
		postfixes = ["valley", "mountain", "city", "river", "smith",  " Creek", " Towers", " Monument", " Settlement"]

		prefix_rnd = randrange(0, len(prefixes) -1, 1)
		postfix_rnd = randrange(0, len(postfixes) -1, 1)
		city_name = prefixes[prefix_rnd] + postfixes[postfix_rnd]
		print("city name: " + city_name)
		return city_name

	# get the name of this city
	def get_name(self):
		return self.name

	def get_player_num(self):
		return self.playerId

	# set the position of this city
	def set_position(self, (pos_x, pos_y)):
		self.pos_x = pos_x
		self.pos_y = pos_y

	# return the position of this city
	def get_position(self):
		return (self.pos_x, self.pos_y)

	# set this cities size
	def set_size(self, size_num):
		self.size = size_num
		self.hp = size_num * 15

	# return this cities size
	def get_size(self):
		return self.size

	# return the name of the city type, depending on its size
	def get_size_name(self):
		if self.city_size <= 0:
			return "Ruins"
		elif self.city_size == 1:
			return "Village"
		elif self.city_size == 2:
			return "City"
		else:
			return "Capital"

	# return the health of thsi city
	def get_hp(self):
		return self.hp

	# start recruiting a new unit
	def recruit_unit(self, unit_blueprint):
		self.production.append(unit_blueprint)
		self.production_time = unit_blueprint.cost_turns
		ev_recruiting_started = CityRecruitmentStartedEvent(self, unit_blueprint)
		EventManager.fire(ev_recruiting_started)

	# return the unit thats actually in production in this city
	def get_unit_in_production(self):
		if (len(self.production) >= 1):
			return self.production[0]
		else:
			return None

	# return True, if a unit in this city is in production
	def is_recruiting(self):
		if len(self.production) >0:
			return True
		return False

	# reduce production time by 1 turn
	def reduce_production_time(self):
		if self.production_time > -1:
			self.production_time -= 1

	def finish_production(self):
		ev_production_finished = CityRecruitmentFinishedEvent(self, self.get_unit_in_production())
		EventManager.fire(ev_production_finished)
		self.production = []
		self.production_time = -1

	def __repr__(self):
		return "<City player="  + str(self.playerId) + " name=" + self.name + " size=" + str(self.get_size_name()) + " pos=" + str(self.get_position()) + " hp=" + str(self.hp) + ">"

	def on_event(self, event):
		# reduce production time on NextTurnEvent
		if isinstance(event, NextTurnEvent):
			self.reduce_production_time()
		# finish production when possible
		if isinstance(event, NextOneEvent):
			if event.actual_player.num == self.playerId and self.production_time == 0:
				self.finish_production()




