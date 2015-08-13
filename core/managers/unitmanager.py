import os
import json
import copy
from random import randrange

from core.entities.unit import Unit, Weapon
from core.entities.tile import Tile

from core.managers.filemanager import FileManager
from core.managers.eventmanager import EventManager
from core.entities.event import *

from core.tools.unitmovementhelper import UnitMovementHelper
from core.managers.locator import Locator

class UnitManager:
	_tag = "[UnitManager] "

	# blueprint & unit list
	_skeletons = {}
	_units = []
	_last_unit_id = -1

	_map = None
	_actual_player = None

	# selected unit cache
	_selected = None
	_selected_moves = []
	_selected_attacks = []

	_selected_city = None

	def __init__(self, tilemap, mod="base"):
		# register in EventManager
		EventManager.register_listener(self)
		# load all unit blueprints
		self.load_unit_skeletons(mod)
		# spawn units from map file
		self._map = tilemap

	# returns a new, unused unit id
	def next_unit_id(self):
		self._last_unit_id += 1
		return self._last_unit_id

	# get the unit on grid position (at_x, at_y), else return None
	def get_unit_at(self, (at_x, at_y), for_specific_player=None):
		for unit in self._units:
			unit_x = int(unit.pos_x)
			unit_y = int(unit.pos_y)
			if unit.pos_x == at_x and unit.pos_y == at_y:
				if not for_specific_player:
					return unit
				elif unit.player_num == for_specific_player:
					return unit
		return None

	# select a unit and fire UnitSelectedEvent
	def select_unit(self, unit):
		self._selected = unit
		# cache & add possible moves and attacks to event
		self._selected_moves = self.get_possible_moves(unit)
		self._selected_attacks = self.get_possible_attacks(unit)
		# fire UnitSelectedEvent
		ev_selected_unit = UnitSelectedEvent(unit, moves=self._selected_moves, attacks=self._selected_attacks)
		EventManager.fire(ev_selected_unit)

	def get_selected_unit(self):
		return self._selected

	def unselect_unit(self):
		self._selected = None
		self._selected_moves = []
		self._selected_attacks = []

	# load all unit skeletons from mods/<mod_name>/units/*.json
	def load_unit_skeletons(self, mod_name):
		unit_folder_path = FileManager.mod_path() + mod_name + "/units/"
		for file in os.listdir(unit_folder_path):
			if file.endswith(".json"):
				# open file and read content
				unit_basename = file.split(".")[0]
				unit_file_path = unit_folder_path + file
				unit_filecontent = FileManager.read_file(unit_file_path)
				# load json content to class
				if unit_filecontent != "":
					unit_json = json.loads(unit_filecontent)
					# load skeleton Unit from json and add it skeleton list
					unit = self.load_unit_skeleton(unit_json)
					unit._basename = unit_basename
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

		unit.cost_turns = unit_json.get("cost_turns", 4)
		unit.cost_gold = unit_json.get("cost_gold", unit.cost_turns *3)

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
		weapon.hit_percent = weapon_json.get("hit_percent", 75)
		weapon.atk_vs_category = weapon_json["atk_vs_category"]
		# weapon.image_path = weapon_json["image_path"]
		return weapon

	# get all units as list
	def get_units(self):
		return self._units

	# get all unit blueprints as list
	def get_unit_blueprints(self):
		skeletons =  []
		for skeleton in self._skeletons.itervalues():
			skeletons.append(skeleton)
		return skeletons

	def get_unit_blueprint(self, blueprint_name):
		return self._skeletons[blueprint_name]

	# get the names of all unit blueprints as list
	def get_skeleton_names(self):
		skeleton_names = []
		for skeleton in self._skeletons:
			skeleton_names.append(skeleton.name)
		return skeleton_names

	# get all units of the player with number player_num as list
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
		EventManager.fire(ev_unit_spawned)

	# move unit to absolute position
	def move_unit_to(self, unit, (to_x, to_y)):
		# translate absolute to relative movement
		rel_x = to_x - unit.pos_x
		rel_y = to_y - unit.pos_y
		# move unit relative to it's position
		self.move_unit(unit, (rel_x, rel_y))

	# unit movement relative to own position; unit movement base method
	def move_unit(self, unit, (rel_x, rel_y)):
		# check if move is possible
		move_in_radius = False
		moves = self.get_possible_moves(unit)
		target_pos = (unit.pos_x + rel_x, unit.pos_y + rel_y)
		way = abs(rel_x) + abs(rel_y)
		# check if move is possible for moved unit
		for movementtile in moves:
			if movementtile.get_position() == target_pos:
				move_in_radius = True
		# move
		if move_in_radius:
			# move unit and reduce mp
			unit.pos_x += rel_x
			unit.pos_y += rel_y
			unit.mp -= way
			#fire UnitMovedEvent
			ev_unit_moved = UnitMovedEvent(unit)
			EventManager.fire(ev_unit_moved)
		return unit

	# attack unit
	def attack_unit(self, attacker, defender):
		# enough mp?
		if attacker.mp >= 1:
			defender_cat = defender.categories[0]
			attack_damage = attacker.weapon.atk_vs_category.get(defender_cat, 0)
			if attack_damage == 0:
				print("[Fight] No damage for category " + defender_cat)
			# roll dice
			hit_percent = attacker.weapon.hit_percent
			rnd_percent = randrange(0, 100, 1)
			print "[Fight] Roll dice: <" + str(hit_percent) + " needed. got " + str(rnd_percent)
			# on hit success
			if (rnd_percent < hit_percent):
				# deal damage & reduce attacker mp
				defender.damage(attack_damage)
				attacker.mp = attacker.mp -1
				print("[Fight] attacker=" + repr(attacker) + " defender=" + repr(defender) + " damage=" + str(attack_damage))
				# destroy defender unit when hp <= 0
				if (defender.hp <= 0):
					# remove unit from unit list
					self.remove_unit(defender)
					# fire UnitKilledEvent
					ev_unit_killed = UnitKilledEvent(defender, attacker)
					EventManager.fire(ev_unit_killed)
					print("[Fight] defender died.")
		# no more mp
		else:
			print("[Fight] no more mp.")

	# remove/kill unit
	def remove_unit(self, unit):
		self._units.remove(unit)
		self._map.units.remove(unit)
		return unit

	# debug method; prints all loaded skeletons
	def print_skeletons(self):
		for unit_name in self._skeletons:
			print (self._tag + "skeleton for " + unit_name + " added.")

	# returns an array with all possible moves of a unit
	def get_possible_moves(self, unit):
		movement_helper = UnitMovementHelper(unit, self._map)
		return movement_helper.get_possible_moves()

	# returns an array with all possible attacks of a unit
	def get_possible_attacks(self, unit):
		attack_distance = unit.weapon.distance
		movement_helper = UnitMovementHelper(unit, self._map, ignore_lds=True)
		# get all tiles the weapon can possibly attack
		possible_attacks = movement_helper.get_possible_moves(distance=attack_distance)
		attacks = []
		for pseudotile in possible_attacks:
			unit_in_rad = self.get_unit_at((pseudotile.pos_x, pseudotile.pos_y))
			# when an enemy unit is on the tile -> add to attacks array
			if unit_in_rad != None and unit_in_rad.player_num != self._actual_player:
				attacks.append(pseudotile)
		return attacks

	def on_event(self, event):
		# on tile selectection: check if a unit is also selected
		if isinstance(event, TileSelectedEvent):
			own_unit_on_tile = self.get_unit_at(event.pos, for_specific_player=self._actual_player)
			print("ownunit=" + repr(own_unit_on_tile))
			if own_unit_on_tile != None:
				self.select_unit(own_unit_on_tile)
			# move or attack with unit
			if own_unit_on_tile == None and self._selected != None:
				moves = self.get_possible_moves(self._selected)
				attacks = self.get_possible_attacks(self._selected)
				print("possible attacks=" + str(len(attacks)))
				action = None
				# selected unit can move to selected tile
				for moveable_tile in moves:
					if moveable_tile.get_position() == event.pos:
						action = "move"
				# selected unit can attack a unit on selected tile
				for attackable_tile in attacks:
					if attackable_tile.get_position() == event.pos:
						action = "attack"
				if action == "attack":
					defender = self.get_unit_at(event.pos)
					attacker = self._selected
					self.attack_unit(attacker, defender)
				elif action == "move":
					self.move_unit_to(self._selected, (event.pos))
				else:
					self.unselect_unit()

		# unit movement on mouse drag
		if isinstance(event, MouseReleasedEvent):
			selected_unit = self.get_selected_unit()
			target_tile_pos = event.gridpos
			if (selected_unit):
				self.move_unit_to(self._selected, target_tile_pos)

		# select unit after movement
		if isinstance(event, UnitMovedEvent):
			moved_unit = event.unit
			self.select_unit(moved_unit)
			Locator.MAP_MGR.select_tile_at(moved_unit.get_position())

		# cache selected city
		if isinstance(event, CitySelectedEvent):
			self._selected_city = event.city

		# when map is loaded
		if isinstance(event, MapLoadedEvent):
			# cache loaded tilemap
			self._map = event.tilemap

		# on right click: unselect actual unit
		if isinstance(event, MouseRightClickedEvent):
			self.unselect_unit()

		# reset unit movement points before player starts
		if isinstance(event, NextOneEvent):
			self._actual_player = event.actual_player.num
			for unit in self.get_units_of_player(self._actual_player):
				unit.reset_mps()