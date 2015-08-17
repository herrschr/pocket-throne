import os
import json
import copy

from core.entities.city import City
from core.entities.building import Building
from core.entities.tile import Tile

from core.managers.filemanager import FileManager
from core.managers.unitmanager import UnitManager
from core.managers.eventmanager import EventManager
from core.entities.event import *

from core.managers.locator import Locator

class CityManager:
	_tag = "[CityManager] "
	_cities = []
	_map = None
	_last_city_id = -1

	_actual_player = None
	_selected = None
	_selected_building = None

	def __init__(self, tilemap, mod="base"):
		# register in EventManager
		EventManager.register_listener(self)
		# spawn units from map file
		self._map = tilemap
		self._cities = tilemap.cities

	# returns all cities; when for_specific_player is set, returns only cities owned by given player num
	def get_cities(self, for_specific_player=None):
		cities = []
		if for_specific_player != None:
			for city in cities:
				if city.get_player_num == for_specific_player:
					cities.append(city)
			return cities
		else:
			return self._cities

	# add a new city
	def add_city_at(self, player_num, size, (at_x, at_y), name=None):
		new_city = City(name=name)
		new_city.set_player_num(player_num)
		new_city.set_size(size)
		new_city.set_position((at_x, at_y))
		new_city._map = self._map
		self._cities.append(new_city)

	# returns a city at the given position
	def get_city_at(self, (at_x, at_y), for_specific_player=None):
		for city in self._cities:
			city_x = int(city.pos_x)
			city_y = int(city.pos_y)
			if city.pos_x == at_x and city.pos_y == at_y:
				if not for_specific_player:
					return city
				elif city.playerId == for_specific_player:
					return city
		return None

	# get building at absolute position when it exists
	def get_building_at(self, (at_x, at_y), for_specific_player=None):
		# get all buildings of the map
		all_buildings = []
		for city in self._cities:
			city_has_wanted_owner = True
			if for_specific_player and city.get_player_num() != for_specific_player:
				city_has_wanted_owner = False
			if city_has_wanted_owner:
				city_buildings = city.get_buildings()
				all_buildings.extend(city_buildings)
		for building in all_buildings:
			if building.get_position() == (at_x, at_y):
				return building
		return None

	# returns all unit blueprints recruitable in a city
	def get_recruitable_units(self, city):
		# get all unit blueprints of the player/fraction
		city_blueprints = []
		fraction_blueprints = Locator.UNIT_MGR.get_unit_blueprints(for_specific_player=city.get_player_num())
		for blueprint in fraction_blueprints:
			# check for required building
			required_building = blueprint.get_required_building()
			if not required_building:
				city_blueprints.append(blueprint)
			else:
				required_building_built = city.has_building(required_building)
				if required_building_built:
					city_blueprints.append(blueprint)
		return city_blueprints

	# set a selected city
	def select_city(self, city):
		# save selected city in CityManager
		self._selected = city
		if city:
			# fire CitySelectedEvent
			recruitable = self.get_recruitable_units(city)
			ev_selected_unit = CitySelectedEvent(city, recruitable=recruitable)
			EventManager.fire(ev_selected_unit)

	# returns selected city
	def get_selected_city(self):
		return self._selected

	# returns if a city is selected
	def has_selected_city(self):
		if self._selected:
			return True
		return False

	# set selected building
	def select_building(self, building):
		# save selected building
		self._selected_building = building
		if building:
			# fire BuildingSelectedEvent
			ev_selected_building = BuildingSelectedEvent(building)
			EventManager.fire(ev_selected_building)

	# returns a new unique city id
	def _next_city_id(self):
		self._last_city_id += 1
		return self._last_city_id

	# recruit a new unit of unit_blueprint type in a city
	def recruit_unit(self, city, unit_blueprint):
		city.recruit_unit(unit_blueprint)

	def on_event(self, event):
		# set actual player on player change
		if isinstance(event, NextOneEvent):
			self._actual_player = event.actual_player.num

		# fire CitySelectedEvent when a tile with a city is selected by the player
		if isinstance(event, TileSelectedEvent):
			selected_city = self.get_city_at(event.pos, for_specific_player=self._actual_player)
			# selected_building =
			if selected_city != None:
				self.select_city(selected_city)

		# unselect city on TileUnselectedEvent
		if isinstance(event, TileUnselectedEvent):
			self.select_city(None)

		# fire CityUnselectedEvent when a tile without a city is selected
		if isinstance(event, MouseRightClickedEvent):
			if self._selected != None:
				# unset selected city
				self.select_city(None)

		# start unit recruition
		if isinstance(event, GuiButtonClickedEvent):
			if event.button_tag.startswith("BUILD-") and self.has_selected_city():
				selected_city = self.get_selected_city()
				recruit_basename = event.button_tag.split("-")[1].lower()
				blueprint = Locator.UNIT_MGR.get_unit_blueprint(recruit_basename)
				self.recruit_unit(selected_city, blueprint)

		# finish unit recruition
		if isinstance(event, CityRecruitmentFinishedEvent):
			# get player, position & type of unit to spawn
			player_num = event.city.get_player_num()
			spawn_pos = event.city.get_position()
			unit_basename = event.blueprint._basename
			# spawn new unit with UnitManager
			Locator.UNIT_MGR.spawn_unit_at(player_num, unit_basename, spawn_pos)
