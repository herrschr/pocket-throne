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

	def __init__(self, tilemap, mod="base"):
		# register in EventManager
		EventManager.register_listener(self)
		# spawn units from map file
		self._map = tilemap
		self._cities = tilemap.cities

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

	def get_recruitable_units(self, city):
		return Locator.UNIT_MGR.get_unit_blueprints()

	def has_selected_city(self):
		if self._selected:
			return True
		return False

	def get_selected_city(self):
		return self._selected

	def next_city_id(self):
		self._last_city_id += 1
		return self._last_city_id

	def recruit_unit(self, city, unit_blueprint):
		city.recruit_unit(unit_blueprint)

	def on_event(self, event):
		# set actual player on player change
		if isinstance(event, NextOneEvent):
			self._actual_player = event.actual_player.num

		# fire CitySelectedEvent when a tile with a city is selected by the player
		if isinstance(event, TileSelectedEvent):
			selected_city = self.get_city_at(event.pos, for_specific_player=self._actual_player)
			if selected_city != None:
				# save selected unit in UnitManager
				self._selected = selected_city
				# fire CitySelectedEvent
				recruitable = self.get_recruitable_units(selected_city)
				ev_selected_unit = CitySelectedEvent(selected_city, recruitable=recruitable)
				EventManager.fire(ev_selected_unit)

		# unselect city on TileUnselectedEvent
		if isinstance(event, TileUnselectedEvent):
			self._selected = None

		# fire CityUnselectedEvent when a tile without a city is selected
		if isinstance(event, MouseRightClickedEvent):
			if self._selected != None:
				# fire CityUnselectedEvent
				self._selected = None
				ev_unselected_city = CityUnselectedEvent()
				EventManager.fire(ev_unselected_city)

		# start unit recruition
		if isinstance(event, GuiButtonClickedEvent):
			if event.button_tag.startswith("BUILD-") and self.has_selected_city():
				selected_city = self.get_selected_city()
				recruit_basename = event.button_tag.split("-")[1].lower()
				blueprint = Locator.UNIT_MGR.get_unit_blueprint(recruit_basename)
				self.recruit_unit(selected_city, blueprint)

		# finish unit recruition
		if isinstance(event, CityRecruitmentFinishedEvent):
			player_num = event.city.get_player_num()
			spawn_pos = event.city.get_position()
			unit_basename = event.blueprint._basename
			Locator.UNIT_MGR.spawn_unit_at(player_num, unit_basename, spawn_pos)
