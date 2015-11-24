import os
import json
import copy

from pocketthrone.entities.city import City
from pocketthrone.entities.building import Building
from pocketthrone.entities.tile import Tile

from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.unitmanager import UnitManager
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WidgetAction, WidgetState

from pocketthrone.managers.locator import Locator

class CityManager:
	_tag = "[CityManager] "
	cities = []
	_last_city_id = -1

	selected_city = None
	selected_building = None

	def __init__(self):
		# register in EventManager
		EventManager.register_listener(self)
		# cache map and city list in CityManager
		tilemap = Locator.MAP_MGR.get_tilemap()
		self.cities = tilemap.cities

	# returns all cities; when for_specific_player is set, returns only cities owned by given player num
	def get_cities(self, for_specific_player=None):
		cities = []
		# when a specific owner is wanted: filter city list for the player first
		if for_specific_player != None:
			for city in cities:
				if city.get_player_num == for_specific_player:
					cities.append(city)
			return cities
		# when no specific owner is wanted: return any town on map
		else:
			return self.cities

	# returns selected city
	def get_selected_city(self):
		return self.selected_city

	# add a new city
	def add_city_at(self, player_num, size, (at_x, at_y), name=None):
		# instanciate new city and set required city properties
		new_city = City(name=name)
		new_city.set_player_num(player_num)
		new_city.set_size(size)
		new_city.set_position((at_x, at_y))
		new_city._map = self._map
		# add new city to CityManagers holder array
		self.cities.append(new_city)

	# returns a city at the given position; when no city is there -> return None
	def get_city_at(self, (at_x, at_y), for_specific_player=None):
		for city in self.cities:
			if city.get_position() == (at_x, at_y):
				# no specific owner is wanted, return city
				if not for_specific_player:
					return city
				# else: filter city for player number
				elif city.playerId == for_specific_player:
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

	# returns all unit blueprints recruitable in a city
	def get_recruitable_units(self, city):
		# get all unit blueprints of the player/fraction
		city_blueprints = []
		fraction_blueprints = Locator.UNIT_MGR.get_unit_blueprints(for_specific_player=city.get_player_num())
		for blueprint in fraction_blueprints:
			# check for required building of any unit type
			required_building = blueprint.get_required_building()
			# when unit type needs no building -> add to list
			if not required_building:
				city_blueprints.append(blueprint)
			# when building requirement is fulfilled -> add to list
			else:
				required_building_built = city.has_building(required_building)
				if required_building_built:
					city_blueprints.append(blueprint)
		return city_blueprints

	# set a selected city
	def select_city(self, city):
		# save selected city in CityManager
		self.selected_city = city
		if city:
			# fire CitySelectedEvent
			recruitable = self.get_recruitable_units(city)
			ev_selected_city= CitySelectedEvent(city, recruitable=recruitable)
			EventManager.fire(ev_selected_city)

	# returns selected city
	def get_selected_city_city(self):
		return self.selected_city

	# returns if a city is selected
	def has_selected_city(self):
		if self.selected_city:
			return True
		return False

	# set selected building
	def select_building(self, building):
		# save selected building
		self.selected_building = building
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
		# reduce player gold
		city.recruit_unit(unit_blueprint)

	def on_event(self, event):
		# fire CitySelectedEvent when a tile with a city is selected by the player
		if isinstance(event, TileSelectedEvent):
			actual_player_num = Locator.PLAYER_MGR.get
			selected_city = self.get_city_at(event.pos, for_specific_player=self._actual_player)
			# selected_building =
			if selected_city != None:
				self.select_city(selected_city)

		# unselect city on TileUnselectedEvent
		if isinstance(event, TileUnselectedEvent):
			self.select_city(None)

		# fire CityUnselectedEvent when a tile without a city is selected
		if isinstance(event, MouseRightClickedEvent):
			if  self.has_selected_city:
				# unset selected city
				self.select_city(None)

		# handle UnitManager relevant button clicks
		if isinstance(event, GuiButtonClickedEvent):
			# recruit unit in selected city when tag is BUILD-* from SideBar
			if event.action == WidgetAction.ACTION_BUILD and self.has_selected_city():
				if event.extra == None:
					print(self._tag + "button extra is null")
				else:
					recruit_basename = event.extra.lower()
					blueprint = Locator.UNIT_MGR.get_unit_blueprint(recruit_basename)
					self.recruit_unit(self.get_selected_city(), blueprint)

		# finish unit recruition
		if isinstance(event, CityRecruitmentFinishedEvent):
			# get player, position & type of unit to spawn
			player_num = event.city.get_player_num()
			spawn_pos = event.city.get_position()
			unit_basename = event.blueprint._basename
			# spawn new unit with UnitManager
			Locator.UNIT_MGR.spawn_unit_at(player_num, unit_basename, spawn_pos, city=event.city)
