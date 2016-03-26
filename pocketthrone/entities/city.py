__all__ = ('City')

from building import Building
from pocketthrone.entities.unit import Unit
from pocketthrone.entities.event import *
from random import choice, seed

from pocketthrone.managers.pipe import L
from pocketthrone.managers.eventmanager import EventManager

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
	_tag = "[City] "

	#names
	name = ""
	name_de = ""

	# resources
	image_path = None
	json_path = None

	# flags
	is_undestroyable = False
	is_owned_by_nature = False

	is_coastal = False
	water_position = None

	# changeable building vars
	player_num = -1
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

	# refactored production
	recruition = None
	construction = None

	def __init__(self, owner_num=-1, name=None, pos=None, size=1, buildings=[], capital=False):
		# set name & hp
		self.hp = 30
		self.player_num = owner_num
		self.name = name
		if name == None:
			self.get_random_name()
		self.size = size
		if pos:
			self.set_position(pos)

	def assign_id(self, _id):
		self._id = _id
		# register as listener in EventManager
		EventManager.register(self)

	def get_random_name(self):
		'''generates a random name for the city'''
		# hard-coded pre- & postifxes for city names
		prefixes = ["S", "Cap", "Fer", "Luc", "Fan", "A", "Grek", "Piac"]
		postfixes = ["andria", "ua", "opolis", "acine", "ticum", "udurum", "ula", "epinum"]
		# fraction city name generation
		print(self._tag + "playernum=" + str(self.player_num))
		fraction = L.PlayerManager.get_player_by_num(self.player_num).get_fraction()
		if fraction:
			city_name = fraction.get_random_city_name()
			self.name = city_name
		else:
			city_name = choice(prefixes) + choice(postfixes)
			self.name = city_name

	def _get_absolute_position(self, rel_pos):
		'''returns absolute position of a position relative to town center'''
		abs_x = self.get_position()[0] + rel_pos[0]
		abs_y = self.get_position()[1] + rel_pos[1]
		return (abs_x, abs_y)

	def _check_for_water(self):
		'''check if the city is near a water tile and set is_coastal'''
		positions = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
		# for each tile besides the city center
		for rel_pos in positions:
			# calculate absolute position
			abs_pos = self._get_absolute_position(rel_pos)
			# check if tile landscape is water
			landscape = L.MapManager.get_tile_at(abs_pos).get_landscape()
			if landscape == "W":
				# set is_coastal True
				self.is_coastal = True
				# set position as usable for harbor
				self.water_position = (rel_pos)
		if self.is_coastal:
			self._build_harbor()

	def _build_harbor(self):
		'''builds an harbor building on a coastal position'''
		self.add_building_at("harbor", self.water_position)

	'''get the name of this city'''
	def get_name(self):
		return self.name

	def set_name(self, name):
		'''set the name of this city'''
		self.name = name

	def get_player_num(self):
		'''get number of the city owner'''
		return self.player_num

	def get_player(self):
		return L.PlayerManager.get_player_by_num(self.player_num)

	# set city owner by player number
	def set_player_num(self, player_num):
		self.player_num = player_num

	def capture(self, player_num):
		'''capture city by player under number player_num'''
		# stop production & set new player
		self.stop_production()
		self.set_player_num(player_num)
		# fire CityCapturedEvent
		ev_city_captured = CityCapturedEvent(self, player_num)
		EventManager.fire(ev_city_captured)

	def get_image_path(self):
		'''get the image path for the town centre'''
		if self.get_size() == 1:
			return "bld_village"
		elif self.get_size() == 2:
			return "bld_city"

	def set_position(self, (pos_x, pos_y)):
		'''set the position of this city'''
		self.pos_x = pos_x
		self.pos_y = pos_y

	def get_position(self):
		'''return the position of this city'''
		return (self.pos_x, self.pos_y)

	def set_size(self, size_num):
		'''set this cities size'''
		self.size = size_num
		self.hp = size_num * 15

	def get_size(self):
		'''returns this cities size'''
		return self.size

	def name_size(self):
		'''return the name of the city type, depending on its size'''
		# (Ruins < Village < City < Capital)
		if self.city_size <= 0:
			return "Ruins"
		elif self.city_size == 1:
			return "Village"
		elif self.city_size == 2:
			return "City"
		else:
			return "Capital"

	def get_hp(self):
		'''return the health of thsi city'''
		return self.hp

	def _recruition(self):
		return L.CityManager.get_recruition_for(self._id)

	def flag_source(self):
		fraction = self.get_player().get_fraction()
		if fraction:
			fraction_name = fraction.basename
			return "flag_" + fraction_name + "_big"
		return "flag_none_big"

	def recruit_unit(self, unit_blueprint):
		'''start recruiting a new unit'''
		# set production and production time
		item_dur = [unit_blueprint, unit_blueprint.cost_turns]
		recruition = self._recruition()
		recruition.append(item_dur)
		print(self._tag + "RECRUIT " + unit_blueprint.get_name() + " in " + self.get_name())
		print(self._tag + "city recrutiton=" + repr(recruition))

	def get_buildings(self):
		'''returns a list of all buildings in this city'''
		blds = []
		for bld in self.buildings:
			if bld.get_city() == self:
				blds.append(bld)
		return blds

	def get_building_at(self, (pos_x, pos_y)):
		'''returns the building at an absolute position when built'''
		building_at = None
		for building in self.get_buildings():
			if building.get_position() == (pos_x, pos_y):
				building_at = building
		return building_at

	def has_building(self, building_type):
		'''returns True when this city has built a building of type building_type'''
		for building in self.get_buildings():
			if building.get_type() == building_type:
				return True
		return False

	def add_building_at(self, building_type, (rel_x, rel_y), flatten_ground=False):
		'''add a building at city position relative position'''
		# calculate absulute building position
		abs_pos = (self.pos_x + rel_x, self.pos_y + rel_y)
		# make building obecjt
		new_bld = Building(self, building_type)
		new_bld.set_position(abs_pos)
		new_bld.rel_x = rel_x
		new_bld.rel_y = rel_y
		# append to building list
		self.buildings.append(new_bld)
		# make dirt ground
		if L.MapManager:
			self._scrape_ground()
		return new_bld

	def add_building(self, building_type):
		'''add a building at a random position inside the city'''
		# get all free building positions
		positions = [(-1,-1), (1,-1), (1,1), (-1,1)]
		print(repr(self.get_buildings()))
		for building in self.get_buildings():
			taken_rel_pos = building.get_relative_position()
			if taken_rel_pos in positions:
				print("buildign at " + str(taken_rel_pos))
				positions.remove(taken_rel_pos)
		# select a random position out of them
		seed()
		rel_pos = choice(positions)
		# build the building a this pos
		self.add_building_at(building_type, rel_pos)

	def add_city_wall(self):
		'''build a wall around this city'''
		# add side walls
		positions = [(-2,-1), (-1,-2), (2,-1), (-1,2)]
		side = 1
		while side <= 4:
			start_pos = positions[side -1]
			self._add_city_wall_line(side, start_pos)
			side += 1
		# add edges of the city wall
		self._add_city_wall_edges()

	def _add_city_wall_line(self, side, (rel_x, rel_y), length=3):
		'''add a city wall on one side of this town'''
		# 1 = left; 2 = top; 3 = right; 4 = bottom
		# set correct wall images
		image_path = None
		gate_image_path = "bld_wall_gate_hor"
		vertically = True
		if side == 1:
			image_path = "bld_wall_left"
		elif side == 2 or side == 4:
			image_path = "bld_wall_hor"
			vertically = False
		elif side == 3:
			image_path = "bld_wall_right"
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

	def _add_city_wall_edges(self):
		'''add the city wall edges to this town'''
		# city wall: relative edge positions
		edge_positions = [(-2,-2), (2,-2), (-2,2), (2,2)]
		# city wall edges: image paths
		edge_img_prefix = "bld_wall_edge_"
		edge_img_postfix = ["lefttop", "righttop", "leftbottom", "rightbottom"]
		# make city wall edges
		i = 0
		while i < 4:
			# calculate absolute building position
			wall_position = edge_positions[i]
			# get full image path of the wall edge
			edge_img_path = edge_img_prefix + edge_img_postfix[i]
			# create wall building and set image_override
			wall_edge = self.add_building_at("wall", wall_position)
			wall_edge.image_override = edge_img_path
			i += 1

	def get_unit_in_production(self):
		'''returns the unit thats actually in production in this city'''
		recruition = self._recruition()
		if recruition:
			return recruition.get_item()
		return None

	def name_production(self):
		'''returns name of unit in production or nothing as string'''
		recruition = self._recruition()
		if not recruition or not recruition.get_item() or not recruition.is_running():
			return "nothing"
		else:
			return recruition.get_item().get_name()


	def is_recruiting(self):
		'''returns True, if a unit in this city is in production'''
		if self._recruition() != None:
			return self._recruition().is_running()
		return False

	def reduce_production_time(self):
		'''reduce production time by 1 turn (called by city on NextTurnEvent)'''
		recruition = self._recruition()
		if recruition:
			recruition.decrease()

	def stop_production(self):
		'''cancel city production (p.e. when its captured)'''
		recruition = self._recruition()
		if recruition:
			recruition.abort()

	def finish_recruition(self, unit):
		# fire CityRecruitmentFinishedEvent
		ev_production_finished = CityRecruitmentFinishedEvent(self, unit)
		EventManager.fire(ev_production_finished)
		# clear production unit and time
		self.stop_production()

	def has_requirement(self, req_name):
		'''check if city has unit requirement'''
		owner_num = self.get_player_num()
		owner_fraction = L.PlayerManager.get_player_by_num(owner_num).get_fraction()
		fraction_basename = owner_fraction.get_basename()
		fraction_req = "is_" + fraction_basename
		# is_<fraction>
		if req_name == fraction_req:
			return True
		# is_coastal
		if req_name == "is_coastal":
			return self.is_coastal
		# has_building
		if req_name.startswith("has_"):
			req_building = req_name.split("_")[1]
			return self.has_building(req_building)
		return False

	def _scrape_ground(self):
		GROUND = "G"
		# scrape ground under city center
		pos = self.get_position()
		tile = L.MapManager.get_tile_at(pos)
		if tile:
			tile.set_landscape(GROUND)
			# scrape ground under buildings
			for bld in self.buildings:
				if bld.get_type() != "harbor":
					pos = bld.get_position()
					tile = L.MapManager.get_tile_at(pos)
					tile.set_landscape(GROUND)

	def __repr__(self):
		'''returns an xml-like string representation of this city'''
		return "<City:" + str(self._id) + " player="  + str(self.player_num) + " name=" + self.name + " size=" + str(self.name_size()) + " pos=" + str(self.get_position()) + " hp=" + str(self.hp) + " water="+ str(self.is_coastal) +  " recruits=" + self.name_production() + ">"

	def on_event(self, event):
		# check for water access
		if isinstance(event, GameStartedEvent):
			self._check_for_water()
			self._scrape_ground()
			if not self.name:
				self.get_random_name()

		# capture city when an enemy player is moving on this city
		if isinstance(event, UnitMovedEvent):
			unit_pos = event.unit.get_position()
			attacker_unit = event.unit
			# when  an enemy unit moves into city center
			if unit_pos == self.get_position() and attacker_unit.get_player_num() != self.get_player_num():
				attacker_player_num = attacker_unit.get_player_num()
				self.capture(attacker_player_num)
		# reduce production time each turn
		if isinstance(event, NextOneEvent):
			if event.actual_player.num == self.get_player_num():
				if self._recruition().is_running():
					self._recruition().decrease()
					print(self._tag + self.get_name() + " prod_id="+ str(self._recruition().parent_id) + " prod -1")
		# finish production when neccessary
		if isinstance(event, ProductionFinishedEvent):
			if event.city._id == self._id:
				if isinstance(event.item, Unit):
					print(self._tag + event.city.get_name() + " FINISHED " + repr(event.item))
					self.finish_recruition(event.item)
		# get random city name when no one is defined
		if isinstance(event, MapLoadedEvent):
			if self.name == None:
				self.get_random_name()


class Production(object):
	def __init__(self, parent_id, ent=None):
		self.items = []
		self.duration = []
		self.ent = ent
		self.parent_id = parent_id
		EventManager.register(self)

	def append(self, item_dur):
		item = item_dur[0]
		dur = item_dur[1]
		self.items.append(item)
		self.duration.append(dur)

	def get_item(self):
		try:
			return self.items[0]
		except:
			return None

	def get_duration(self):
		try:
			return self.duration[0]
		except:
			return None

	def is_running(self):
		if len(self.items) > 0:
			return True
		return False

	def decrease(self, num=1):
		if self.is_running():
			self.duration[0] -= num
			if self.duration[0] < 1:
				self._item_finished(self.items[0])

	def abort(self):
		self.items = []
		self.duration = []

	def next(self):
		pass

	def _item_finished(self, item):
		parent = L.CityManager.get_city_by_id(self.parent_id)
		ev_prod_finished = ProductionFinishedEvent(parent, item)
		EventManager.fire(ev_prod_finished)
		self.abort()

	def on_event(self, event):
		pass

	def __repr__(self):
		return "<Production city_id=" + str(self.parent_id) + " list=" + repr(self.items) + " durs=" + repr(self.duration) + ">"
