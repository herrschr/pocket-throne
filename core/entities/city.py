from building import Building
from core.entities.unit import Unit
from core.entities.event import *
from random import choice, seed

from core.managers.locator import Locator
from core.managers.eventmanager import EventManager

# city wall and building positions (N = Wall, L = Street, O = Building)
#	NNNNN
#	NOLON
#	NLOLN
#	NOLON
#	NNNNN

class City:
	# engine properties
	_id = -1
	_map = None

	#names
	name = ""
	name_de = ""

	# resources
	image_path = None
	json_path = None

	# flags
	is_undestroyable = False
	is_owned_by_nature = False

	# changeable building vars
	playerId = -1
	city_size = 1
	hp = -1
	region = None
	pos_x = -1
	pos_y = -1

	# buildings
	buildings = []

	# production
	production = []
	production_time = -1

	def __init__(self, name=None, buildings=[], capital=False):
		# register as listener in EventManager
		EventManager.register_listener(self)
		# set name & hp
		self.hp = 30
		if not name:
			self.name = self.get_random_name()
		else:
			self.name = name
		# eventually add buildings
		for building_type in buildings:
			self.add_building(building_type)

	# generates a random name for the city
	def get_random_name(self):
		# hard-coded pre- & postifxes for city names
		prefixes = ["Iron", "Green", "Wood", "Wild", "Dried",  "Old", "New", "Saint", "Death"]
		postfixes = ["valley", "mountain", "city", "river", "smith",  " Creek", " Towers", " Monument", " Settlement"]
		# select one of each
		seed()
		prefix = choice(prefixes)
		seed()
		postfix = choice(postfixes)
		# put them together & return the city name
		city_name = prefix + postfix
		return city_name

	# get the name of this city
	def get_name(self):
		return self.name

	# set the name of this city
	def set_name(self, name):
		self.name = name

	# get number of the city owner
	def get_player_num(self):
		return self.playerId

	# set city owner by player number
	def set_player_num(self, player_num):
		self.playerId = player_num

	# city is captured by a new player
	def capture(self, player_num):
		# strop production & set new player
		self.stop_production()
		self.set_player_num(player_num)
		# fire CityCapturedEvent
		ev_city_captured = CityCapturedEvent(self, player_num)
		EventManager.fire(ev_city_captured)

	# get the image path for the town centre
	def get_image_path(self):
		if self.get_size() == 1:
			return "city_village.png"
		elif self.get_size() == 2:
			return "city_city.png"

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

	# return the name of the city type, depending on its size (Ruins < Village < City < Capital)
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
		# set production and production time
		self.production.append(unit_blueprint)
		self.production_time = unit_blueprint.cost_turns
		# fire CityRecruitmentStartedEvent
		ev_recruiting_started = CityRecruitmentStartedEvent(self, unit_blueprint)
		EventManager.fire(ev_recruiting_started)

	# returns all buildings of this city
	def get_buildings(self):
		return self.buildings

	# returns the building at an absolute position when built
	def get_building_at(self, (pos_x, pos_y)):
		building_at = None
		for building in self.get_buildings():
			if building.get_position() == (pos_x, pos_y):
				building_at = building
		return building_at

	# returns True when this city has built a building of type building_type
	def has_building(self, building_type):
		for building in self.get_buildings():
			if building.get_type() == building_type:
				return True
		return False

	# add a building at city position relative position
	def add_building_at(self, building_type, (rel_x, rel_y)):
		# calculate absulute building position
		abs_pos = (self.pos_x + rel_x, self.pos_y + rel_y)
		new_bld = Building(self, building_type)
		new_bld.set_position(abs_pos)
		new_bld.rel_x = rel_x
		new_bld.rel_y = rel_y
		self.buildings.append(new_bld)
		return new_bld

	# add a building at a random position inside the city
	def add_building(self, building_type):
		# get all free building positions
		positions = [(-1,-1), (1,-1), (1,1), (-1,1)]
		for building in self.get_buildings():
			taken_rel_pos = building.get_relative_position()
			if taken_rel_pos in positions:
				print("city " + self.name + ": " + str(taken_rel_pos) + " isnt free")
				positions.remove(taken_rel_pos)
		# select a random position out of them
		seed()
		rel_pos = choice(positions)
		# build the building a this pos
		self.add_building_at(building_type, rel_pos)

	# build a wall around this city
	def add_city_wall(self):
		# add side walls
		positions = [(-2,-1), (-1,-2), (2,-1), (-1,2)]
		side = 1
		while side <= 4:
			start_pos = positions[side -1]
			self._add_city_wall_line(side, start_pos)
			side += 1
		self._add_city_wall_edges()

	# add a city wall on one side of this town
	# 1 = left; 2 = top; 3 = right; 4 = bottom
	def _add_city_wall_line(self, side, (rel_x, rel_y), length=3):
		# set correct wall images
		image_path = None
		gate_image_path = "city_wall_gate_hor.png"
		vertically = True
		if side == 1:
			image_path = "city_wall_left.png"
		elif side == 2 or side == 4:
			image_path = "city_wall_hor.png"
			vertically = False
		elif side == 3:
			image_path = "city_wall_right.png"
		# make a city wall line
		i = 0
		while i < length:
			# get tile at wall position
			wall = self.add_building_at("wall", (rel_x, rel_y))
			# set correct image paths in image_override of the wall building
			wall.image_override = image_path
			if vertically:
				rel_y += 1
			else:
				rel_x += 1
				# make wall gates on top & bottom of an horizontal wall
				if i == 1:
					wall.image_override = gate_image_path
			i += 1

	# add the city wall edges to this town
	def _add_city_wall_edges(self):
		# city wall: relative edge positions
		edge_positions = [(-2,-2), (2,-2), (-2,2), (2,2)]
		# city wall edges: image paths
		edge_img_prefix = "city_wall_edge_"
		edge_img_postfix = ["lefttop", "righttop", "leftbottom", "rightbottom"]
		# make city wall edges
		i = 0
		while i < 4:
			# calculate absolute building position
			wall_position = edge_positions[i]
			# get full image path of the wall edge
			edge_img_path = edge_img_prefix + edge_img_postfix[i] + ".png"
			# create wall building and set image_override
			wall_edge = self.add_building_at("wall", wall_position)
			wall_edge.image_override = edge_img_path
			i += 1

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

	# reduce production time by 1 turn (called by city on NextTurnEvent)
	def reduce_production_time(self):
		if self.production_time > -1:
			self.production_time -= 1

	# cancel city production (p.e. when its captured)
	def stop_production(self):
		self.production = []
		self.production_time = -1

	# finish city production (eventually called on NextOneEvent)
	def finish_production(self):
		# fire CityRecruitmentFinishedEvent
		ev_production_finished = CityRecruitmentFinishedEvent(self, self.get_unit_in_production())
		EventManager.fire(ev_production_finished)
		# clear production unit and time
		self.production = []
		self.production_time = -1

	def __repr__(self):
		return "<City player="  + str(self.playerId) + " name=" + self.name + " size=" + str(self.get_size_name()) + " pos=" + str(self.get_position()) + " hp=" + str(self.hp) + ">"

	def on_event(self, event):
		# capture city when an enemy player is moving on this city
		if isinstance(event, UnitMovedEvent):
			unit_pos = event.unit.get_position()
			# when  an enemy unit moves into city center
			if unit_pos == self.get_position() and unit.get_player_num != self.get_player_num():
				attacker_unit = event.unit
				attacker_player_num = attacker_unit.get_player_num()
				self.capture(attacker_player_num)

		# reduce production time on NextTurnEvent
		if isinstance(event, NextTurnEvent):
			self.reduce_production_time()
		# finish production when possible
		if isinstance(event, NextOneEvent):
			if event.actual_player.num == self.playerId and self.production_time == 0:
				self.finish_production()




