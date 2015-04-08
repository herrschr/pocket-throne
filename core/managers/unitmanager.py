import os
import json
import copy
from core.entities.unit import Unit, Weapon
from core.managers.filemanager import FileManager
from core.managers.eventmanager import EventManager
from core.entities.event import *

class UnitManager:
	_tag = "UnitManager: "
	_skeletons = {}
	_units = []
	_map = None
	_last_unit_id = -1

	_selected = None

	def __init__(self, eventmanager, tilemap, mod="base"):
		# register in EventManager
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)

		# ignore the mod name, no active modding system
		# load all unit blueprints
		self.load_unit_skeletons("base")

		# spawn units from map file
		self._map = tilemap

	# returns a new, unused unit id
	def next_unit_id(self):
		self._last_unit_id += 1
		return self._last_unit_id

	def get_unit_at(self, (at_x, at_y)):
		for unit in self._units:
			unit_x = int(unit.pos_x)
			unit_y = int(unit.pos_y)
			if unit.pos_x == at_x and unit.pos_y == at_y:
				return unit
		return None

	# load unit skeletons from mods/<mod_name>/units/*.json
	def load_unit_skeletons(self, mod_name):
		unit_folder_path = FileManager.mod_path() + mod_name + "/units/"
		for file in os.listdir(unit_folder_path):
			if file.endswith(".json"):
				# load json file
				unit_basename = file.split(".")[0]
				unit_file_path = unit_folder_path + file
				unit_json = json.loads(FileManager.read_file(unit_file_path))
				# load skeleton Unit from json and add it skeleton list
				unit = self.load_unit_skeleton(unit_json)
				self._skeletons[unit_basename] = unit
		self.print_skeletons()

	# fill a Unit skeleton with a json dict
	def load_unit_skeleton(self, unit_json):
		# load basic values and fill Unit
		unit_name = unit_json["name"]
		unit = Unit(unit_name)
		unit.name_de = unit_json["name_de"]
		unit.categories = unit_json["categories"]
		unit.image_path = unit_json["image"]
		unit.health = unit_json["health"]
		unit.movement = unit_json["movement"]

		# load maximal amount per player
		max_per_player = unit_json["max_per_player"]
		if (max_per_player == -1):
			unit.has_player_max = False
			unit.max_per_player = -1
		else:
			unit.has_player_max = True
			unit.max_per_player = max_per_player

		# load maximal amount on the whole map
		max_per_map = unit_json["max_per_map"]
		if (max_per_map == -1):
			unit.has_map_max = False
			unit.max_per_map = -1
		else:
			unit.has_map_max = True
			unit.max_per_map = max_per_map

		# add weapon & return finished unit
		weapon = self.load_weapon(unit_json)
		unit.give_weapon(weapon)
		return unit

	# load a weapon from a unit's json dict
	def load_weapon(self, unit_json):
		weapon_json = unit_json["weapon"]
		weapon = Weapon()
		weapon.name = weapon_json["name"]
		weapon.name_de = weapon_json["name_de"]
		weapon.value = weapon_json["value"]
		weapon.distance = weapon_json["distance"]
		weapon.atk_vs_category = weapon_json["atk_vs_category"]
		# weapon.image_path = weapon_json["image_path"]
		return weapon

	def get_units(self):
		return self._units

	def get_units_of_player(self, player_num):
		units_of_player = []
		for unit in self._units:
			if unit.player_num == player_num:
				units_of_player.append(unit)
		return units_of_player


	# get a prefilled Unit class from loaded skeleton/blueprint
	def get_prefilled_unit(self, unit_basename):
		return copy.deepcopy(self._skeletons[unit_basename])

	# spawn a new unit with given player and position
	def spawn_unit_at(self, player_num, unit_basename, (pos_x, pos_y)):
		# get prefilled unit and unit id
		to_spawn = self.get_prefilled_unit(unit_basename)
		to_spawn._id = self.next_unit_id()
		# set hp & mp
		to_spawn.hp = to_spawn.health
		to_spawn.mp = to_spawn.movement
		# set player and pos
		to_spawn.player_num = player_num
		to_spawn.set_position((pos_x, pos_y))
		# add unit to self._units and _map._units
		self._units.append(to_spawn)
		self._map.units.append(to_spawn)
		# fire UnitSpawnedEvent
		ev_unit_spawned = UnitSpawnedEvent(to_spawn, (pos_x, pos_y))
		self._eventmgr.fire(ev_unit_spawned)

	# move unit to absolute position
	def move_unit_to(self, unit, (to_x, to_y)):
		# get relative movement
		rel_x = to_x - unit.pos_x
		rel_y = to_y - unit.pos_y
		# weird undocumented movement hacking
		if rel_x != 0 and rel_y != 0:
			if rel_x > rel_y:
				rel_y = 0
			if rel_y > rel_x:
				rel_x = 0
		# move unit relative to it's position
		self.move_unit(unit, (rel_x, rel_y))

	# unit movement relative to own position; unit movement base method
	def move_unit(self, unit, (rel_x, rel_y)):
		if unit.mp <= 0:
			print ("UnitManager: unit " + unit.name + " has no more mp")
			return
		# restrict two-direction movement, not allowed yet
		if rel_x != 0 and rel_y != 0:
			print ("UnitManager: no two-direction movement of units allowed")
			return
		# horizontal movement
		elif rel_x != 0 and rel_y == 0:
			# check if way is too long
			way = abs(rel_x)
			if way > unit.mp:
				print ("UnitManager: unit " + unit.name + " isn't allowed to move " + str(way) + " tiles")
				return
			unit.pos_x += rel_x
			unit.mp -= abs(rel_x)
		# vertical movement
		elif rel_x == 0 and rel_y != 0:
			# check if way is too long
			way = abs(rel_y)
			if way > unit.mp:
				print ("UnitManager: unit " + unit.name + " isn't allowed to move " + str(way) + " tiles")
				return
			unit.pos_y += rel_y
			unit.mp -= abs(rel_y)
		return unit

	# remove/kill unit
	def remove_unit(self, unit):
		self._units.remove(unit)
		self._map.units.remove(unit)
		return unit

	# debug method; prints all loaded skeletons
	def print_skeletons(self):
		for unit_name in self._skeletons:
			print (self._tag + "skeleton for " + unit_name + " added.")

	def on_event(self, event):
		# on tile selectection: check if a unit is also selected
		if isinstance(event, TileSelectedEvent):
			selected_unit = self.get_unit_at(event.pos)
			if selected_unit != None:
				# save selectec unit in UnitManager
				self._selected = selected_unit
				# fire UnitSelectedEvent
				ev_selected_unit = UnitSelectedEvent(selected_unit)
				self._eventmgr.fire(ev_selected_unit)
			# move unit
			if selected_unit == None and self._selected != None:
				print("move?")
				self.move_unit_to(self._selected, (event.pos))

		# on right click: unselect actual unit
		if isinstance(event, MouseRightClickedEvent):
			if self._selected != None:
				# fire UnitUnselectedEvent
				self._selected = None
				ev_unselected_unit = UnitUnselectedEvent()
				self._eventmgr.fire(ev_unselected_unit)

		# reset unit movement points before player starts
		if isinstance(event, NextOneEvent):
			actual_player_num = event.actual_player.num
			for unit in self.get_units_of_player(actual_player_num):
				unit.reset_mps()



