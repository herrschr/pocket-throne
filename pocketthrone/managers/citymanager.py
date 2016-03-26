import os
import json

from pocketthrone.entities.city import City, Production
from pocketthrone.entities.building import Building
from pocketthrone.entities.tile import Tile

from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.unitmanager import UnitManager
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetAction, WidgetState

from pocketthrone.managers.pipe import L

class CityManager:
	_tag = "[CityManager] "
	_last_city_id = -1

	cities = {}
	recruitions = {}
	constructions = {}

	selected_city = None
	selected_building = None

	def __init__(self):
		# register in EventManager
		EventManager.register(self)

	def add_cities(self, city_list):
		'''adds cities from given city lis tand assigns an id for each one'''
		for city in city_list:
			# assign id
			_id = self._next_city_id()
			city.assign_id(_id)
			# add to city list
			self.cities[_id] = city
			self.recruitions[_id] = Production(_id, ent="unit")
			print(self._tag + "added under id " + str(_id) + ": " + repr(city))

	def get_cities(self, for_specific_player=None):
		'''returns all cities; when for_specific_player is set, returns only cities owned by given player num'''
		cities = []
		# when a specific owner is wanted: filter city list for the player first
		if for_specific_player != None:
			for city in self.cities.values():
				if city.get_player_num() == for_specific_player:
					cities.append(city)
			return cities
		# when no specific owner is wanted: return any town on map
		else:
			return self.cities.values()

	def get_cities_by_player(self, player_num):
		'''returns cities owned by player with player_id'''
		filtered = []
		for city in self.cities.values():
			if city.get_player_num() == player_num:
				filtered.append(city)
		return filtered

	def get_city_by_id(self, city_id):
		try:
			return self.cities[city_id]
		except:
			return None

	# returns selected city
	def get_selected_city(self):
		return self.selected_city

	# add a new city
	def add_city_at(self, player_num, size, (at_x, at_y), name=None):
		# instanciate new city and set required city properties
		_id = self._next_city_id()
		new_city = City(name=name)
		new_city.assign_id(_id)
		new_city.set_player_num(player_num)
		new_city.set_size(size)
		new_city.set_position((at_x, at_y))
		new_city._map = self._map
		# add new city to CityManagers holder array
		self.cities.append(new_city)

	# returns a city at the given position; when no city is there -> return None
	def get_city_at(self, (at_x, at_y), for_specific_player=None):
		for city in self.cities.values():
			if city.get_position() == (at_x, at_y):
				# no specific owner is wanted, return city
				if not for_specific_player:
					return city
				# else: filter city for player number
				elif city.player_num == for_specific_player:
					return city
		return None

	# get any building at absolute position when it exists
	def get_building_at(self, (x, y), for_specific_player=None):
		cities = []
		all_buildings = []
		# get any cities or cities of wanted owner
		cities = self.get_cities(for_specific_player=for_specific_player)
		# add buildings of any city into a list
		for city in cities:
			city_buildings = city.get_buildings()
			all_buildings.extend(city_buildings)
		# filter building list for building with wanted position
		for building in all_buildings:
			if building.get_position() == (x, y):
				return building
		return None

	def get_recruitable_units(self, city):
		'''returns all unit blueprints recruitable in a city'''
		# get all unit blueprints of the player/fraction
		city_blueprints = []
		city_player_num = city.get_player_num()
		blueprints = L.UnitManager.get_blueprints()
		for blueprint in blueprints:
			is_able = True
			#check selected city requirements
			for requirement in blueprint.requirements:
				has_requirement = city.has_requirement(requirement)
				if not has_requirement:
					is_able = False
			if is_able:
				city_blueprints.append(blueprint)
		return city_blueprints

	def select_city(self, city):
		'''sets city as selected'''
		# save selected city in CityManager
		self.selected_city = city
		if city:
			# fire CitySelectedEvent for_specific_player=city.get_player_num())
			ev_selected_city= CitySelectedEvent(city)
			EventManager.fire(ev_selected_city)

	def has_selected_city(self):
		'''returns if a city is selected'''
		if self.selected_city:
			return True
		return False

	def select_building(self, building):
		'''set selected building'''
		# save selected building
		self.selected_building = building
		if building:
			# fire BuildingSelectedEvent
			ev_selected_building = BuildingSelectedEvent(building)
			EventManager.fire(ev_selected_building)

	def _next_city_id(self):
		'''returns a new unique city id'''
		self._last_city_id += 1
		return self._last_city_id

	def recruit_unit(self, city, unit_blueprint):
		'''recruits a new unit of unit_blueprint type in a city'''
		# reduce player gold
		city.recruit_unit(unit_blueprint)

	def get_recruition_for(self, city_id):
		try:
			return self.recruitions[city_id]
		except:
			print(self._tag + "cant recruit in {}".format(city_id))
			return None

	def on_event(self, event):
		if isinstance(event, MapLoadedEvent):
			self.tilemap = event.tilemap
			# cache map and city list in CityManager
			self.add_cities(event.tilemap.cities)
		# fire CitySelectedEvent when a tile with a city is selected by the player
		if isinstance(event, TileSelectedEvent):
			actual_player_num = L.PlayerManager.get_actual_player_num()
			selected_city = self.get_city_at(event.pos, for_specific_player=actual_player_num)
			# selected_building =
			if selected_city != None:
				self.select_city(selected_city)

		# unselect city on TileUnselectedEvent
		if isinstance(event, TileUnselectedEvent):
			self.select_city(None)
		# decrease production time
		if isinstance(event, NextOneEvent):
			player_id = event.actual_player
			player_cities = self
		# fire CityUnselectedEvent when a tile without a city is selected
		if isinstance(event, MouseRightClickedEvent):
			if  self.has_selected_city:
				# unset selected city
				self.select_city(None)

		# finish unit recruition
		if isinstance(event, CityRecruitmentFinishedEvent):
			# get player, position & type of unit to spawn
			player_num = event.city.get_player_num()
			# TODO spawn beside city
			spawn_pos = event.city.get_position()
			unit_basename = event.blueprint.basename
			# spawn new unit with UnitManager
			L.UnitManager.spawn_unit_at(player_num, unit_basename, spawn_pos, city=event.city)
