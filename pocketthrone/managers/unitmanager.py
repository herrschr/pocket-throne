import os
import json
import copy
from random import randrange

from pocketthrone.entities.unit import Unit
from pocketthrone.entities.weapon import Weapon
from pocketthrone.entities.tile import Tile

from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.entities.event import *
from pocketthrone.entities.enum import WeaponType, UnitType

from pocketthrone.tools.unitmovementhelper import UnitMovementHelper
from pocketthrone.managers.locator import Locator

class UnitManager:
	_tag = "[UnitManager] "
	_last_unit_id = -1

	# blueprint & unit list
	blueprints = {}
	units = []

	# selected unit cache
	selected_unit = None
	selected_unit_moves = []
	selected_unit_attacks = []

	def __init__(self):
		EventManager.register_listener(self)
		# load all unit blueprints
		mod_name = Locator.MOD_MGR.get_selected_mod()._basename
		self.load_unitblueprints(mod_name)
		# spawn units from map file
		self._spawn_units_from_map()

	# spawn units from the TileMap at UnitManager initialization
	def _spawn_units_from_map(self):
		map_units = Locator.MAP_MGR.get_tilemap().units
		for unit in map_units:
			self.spawn_unit_at(unit.get_player_num(), unit.get_type(), unit.get_position())
		print(self._tag + "spawned " + str(map_units.size()))

	# returns a new, unused unit id
	def next_unit_id(self):
		self._last_unit_id += 1
		return self._last_unit_id

	# get the unit on grid position (at_x, at_y), else return None
	def get_unit_at(self, (at_x, at_y), for_specific_player=None):
		for unit in self.units:
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
		self.selected_unit = unit
		# cache & add possible moves and attacks to event
		self.selected_unit_moves = self.get_possible_moves(unit)
		self.selected_unit_attacks = self.get_possible_attacks(unit)
		# fire UnitSelectedEvent
		ev_selected_unit = UnitSelectedEvent(unit, moves=self.selected_unit_moves, attacks=self.selected_unit_attacks)
		EventManager.fire(ev_selected_unit)

	def get_selected_unit(self):
		return self.selected_unit

	def has_selected_unit(self):
		if self.selected_unit:
			return True
		return False

	def unselect_unit(self):
		self.selected_unit = None
		self.selected_unit_moves = []
		self.selected_unit_attacks = []

	# load all unit skeletons from mods/<mod_name>/units/*.json
	def load_unitblueprints(self, mod_name):
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
					unit = self.load_unit_skeleton(unit_json, unit_basename)
					self.blueprints[unit_basename] = unit
		self.print_blueprints()

	# returns a unit blueprint from unit json object
	def load_unit_skeleton(self, unit_json, unit_basename):
		# load engine properties and fill in a new unit object
		unit = Unit(unit_basename)
		unit.is_disabled = unit_json.get("disabled", False)
		unit.name = unit_json["name"]
		unit.name_de = unit_json["name_de"]
		unit.image_path = unit_json["image"]
		# load unit specific properties
		unit.health = unit_json["health"]
		unit.movement = unit_json["movement"]
		# load fighting properties
		unit._unit_type = unit_json["type"]
		unit._category = unit_json["category"]
		# load production costs
		unit.cost_turns = unit_json.get("cost_turns", 4)
		unit.cost_gold = unit_json.get("cost_gold", unit.cost_turns *3)
		# load unit requirements
		unit.required_building = unit_json.get("required_building", None)
		unit.required_fraction = unit_json.get("required_fraction", None)
		# load maximal amount per player & map
		unit.max_per_player = unit_json.get("max_per_player", None)
		unit.max_per_map = unit_json.get("max_per_map", None)
		# add weapon & return finished unit
		weapon = self.load_weapon(unit_json)
		unit.give_weapon(weapon)
		return unit

	# returns a weapon from a unit json object
	def load_weapon(self, unit_json):
		# get the weapon json object out of the unit json object
		weapon_json = unit_json["weapon"]
		weapon_category = weapon_json["category"]
		weapon = Weapon(weapon_category)
		# fill weapon with required properties
		weapon.name = weapon_json["name"]
		weapon.name_de = weapon_json["name_de"]
		# fill weapon with fighting properties
		weapon.distance = weapon_json["distance"]
		weapon.hit_chance = weapon_json.get("hit_chance", 50)
		weapon.damage = weapon_json["damage"]
		weapon.multiplier_vs_category = weapon_json.get("multiplier_vs_category", {})
		weapon.merge_attack_multipliers()
		return weapon

	# get all units as list
	def get_units(self):
		return self.units

	# get a list of enabled unit blueprints
	def get_unit_blueprints(self, for_specific_player=None, add_disabled=False):
		enabled_blueprints =  []
		blueprints = []
		# filter deisabled blueprints
		if add_disabled:
			enabled_blueprints = self.get_all_blueprints()
		else:
			for blueprint in self.get_all_blueprints():
				if not blueprint.is_disabled:
					enabled_blueprints.append(blueprint)
		# when for_specific_player is none: return all unit blueprints
		if not for_specific_player:
			for blueprint in enabled_blueprints:
				blueprints.append(blueprint)
		# else return only blueprints recruitable by a specific player num
		else:
			# get the fraction name of player number in for_specific_player
			player = Locator.PLAYER_MGR.get_player_by_num(for_specific_player)
			player_fraction_name = player.get_fraction()._basename
			for blueprint in enabled_blueprints:
				req_fraction = blueprint.get_required_fraction()
				# add blueprint when no fraction is required
				if not req_fraction:
					blueprints.append(blueprint)
				# add blueprint when player has required fraction for the unit
				elif req_fraction == player_fraction_name:
					blueprints.append(blueprint)
		return blueprints

	# returns blueprints as a list, ignore if enabled
	def get_all_blueprints(self):
		blueprints = []
		for blueprint in self.blueprints.itervalues():
			blueprints.append(blueprint)
		return blueprints

	# returns a single unit blueprint by its basename
	def get_unit_blueprint(self, blueprint_name):
		return self.blueprints[blueprint_name]

	# returns the names of all unit blueprints as list
	def get_blueprint_names(self):
		blueprint_names = []
		for blueprint in self.get_unit_blueprints():
			blueprint_names.append(blueprint.get_name())
		return blueprint_names

	# get all units of the player with number player_num as list
	def get_units_of_player(self, player_num):
		units_of_player = []
		for unit in self.units:
			if unit.player_num == player_num:
				units_of_player.append(unit)
		return units_of_player


	# get a prefilled Unit class from loaded skeleton/blueprint
	def get_prefilled_unit(self, unit_basename):
		return copy.deepcopy(self.blueprints[unit_basename])

	# spawn a new unit with given player and position
	def spawn_unit_at(self, player_num, unit_basename, (pos_x, pos_y), city=None):
		# get prefilled unit and unit id
		to_spawn = self.get_prefilled_unit(unit_basename)
		to_spawn._id = self.next_unit_id()
		# set hp & mp
		to_spawn.city = city
		to_spawn.hp = to_spawn.health
		to_spawn.mp = to_spawn.movement
		# set player and pos
		to_spawn.player_num = player_num
		to_spawn.set_position((pos_x, pos_y))
		# add unit to self.units and _map.units
		self.units.append(to_spawn)
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
		starting_pos = unit.get_position()
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
			ev_unit_moved = UnitMovedEvent(unit, starting_pos)
			EventManager.fire(ev_unit_moved)
		return unit

	# attack unit
	def attack_unit(self, attacker, defender):
		# enough mp? (2 required)
		if attacker.mp >= 2:
			# calculate wepon damage vs. defender unit type
			defender_type = defender.unit_type
			attack_damage = attacker.weapon.get_damage_vs(defender_type)
			if attack_damage == 0:
				print("[Fight] Aborted. No damage vs. category " + defender_type)
			# reduce attacker's mp
			attacker.mp = attacker.mp -2
			# roll dice
			req_percent = 100 - attacker.weapon.hit_chance
			rnd_percent = randrange(0, 100, 1)
			print "[Fight] Dice roll: got " + str(rnd_percent) + " of " + str(req_percent)
			# on hit success
			if (rnd_percent > req_percent):
				# deal damage & reduce attacker mp
				defender.damage(attack_damage)
				print("[Fight] attacker=" + repr(attacker) + " defender=" + repr(defender) + " damage=" + str(attack_damage))
				# destroy defender unit when hp <= 0
				if (defender.hp <= 0):
					print("[Fight] defender died.")
					# remove unit from unit list
					self.remove_unit(defender)
					# fire UnitKilledEvent
					ev_unit_killed = UnitKilledEvent(defender, attacker)
					EventManager.fire(ev_unit_killed)
		# not enough mp left for an attack
		else:
			print("[Fight] Aborted. Not enough mp left.")

	# remove/kill unit
	def remove_unit(self, unit):
		self.units.remove(unit)
		return unit

	# debug method; prints all loaded skeletons
	def print_blueprints(self):
		prefix = "blueprints = [ "
		postfix = " ]"
		blueprints = ""
		for basename in self.blueprints:
			blueprints += basename + ", "
		print(self._tag + prefix + blueprints + postfix)

	# returns an array with all possible moves of a unit
	def get_possible_moves(self, unit):
		# load TileMap from MapManager
		tilemap = Locator.MAP_MGR.get_tilemap()
		movement_helper = UnitMovementHelper(unit, self.tilemap)
		possible_moves = movement_helper.get_possible_moves()
		# remove tiles with own unit
		for pseudotile in possible_moves:
			unit_on_tile = self.get_unit_at((pseudotile.pos_x, pseudotile.pos_y))
			if unit_on_tile:
				possible_moves.remove(pseudotile)
		return possible_moves

	# returns an array with all possible attacks of a unit
	def get_possible_attacks(self, unit):
		tilemap = Locator.MAP_MGR.get_tilemap()
		attack_distance = unit.weapon.distance
		movement_helper = UnitMovementHelper(unit, tilemap)
		# get all tiles the weapon can possibly attack
		possible_attacks = movement_helper.get_possible_moves(distance=attack_distance)
		attacks = []
		for pseudotile in possible_attacks:
			unit_on_tile = self.get_unit_at((pseudotile.pos_x, pseudotile.pos_y))
			# when an enemy unit is on the tile -> add to attacks array
			if unit_on_tile != None and unit_on_tile.player_num != self._actual_player:
				attacks.append(pseudotile)
		return attacks

	def on_event(self, event):
		# on tile selectection: check if a unit is also selected
		if isinstance(event, TileSelectedEvent):
			is_own_unit = False
			unit_on_tile = self.get_unit_at(event.pos)
			# when a tile with a unit on it is selected
			if unit_on_tile:
				# unit is own -> select it
				if unit_on_tile.get_player_num() == self._actual_player:
					self.select_unit(unit_on_tile)
					return;
				# unit isnt own -> attack when possible
				else:
					# abort attack check when no unit is selected
					if not self.hasselected_unit_unit():
						return;
					# check if an attack on event.pos is possible for selected unit
					for attack_tile in self.selected_unit_attacks:
						if attack_tile.get_position() == event.pos:
							defender = unit_on_tile
							attacker = self.getselected_unit_unit()
							# attack with selected unit
							self.attack_unit(attacker, defender)
							return;
			# when no unit stands on tile -> move when possible
			elif not unit_on_tile:
				# abort movement check when no unit is selected
				if not self.hasselected_unit_unit():
					return;
				# check if selected unit move is possible
				for move_tile in self.selected_unit_moves:
					if move_tile.get_position() == event.pos:
						# move unit to event pos
						self.move_unit_to(self.getselected_unit_unit(), (event.pos))
						return;
				# when no action was made -> unselect unit
				self.unselect_unit()

		# unit movement on mouse drag
		if isinstance(event, MouseReleasedEvent):
			selected_unit = self.getselected_unit_unit()
			target_tile_pos = event.gridpos
			unit_on_tile = self.get_unit_at(target_tile_pos)
			# when no unit is on target tile: move
			if selected_unit and not unit_on_tile:
				self.move_unit_to(self.selected_unit, target_tile_pos)

		# select unit after movement
		if isinstance(event, UnitMovedEvent):
			moved_unit = event.unit
			self.select_unit(moved_unit)
			Locator.MAP_MGR.select_tile_at(moved_unit.get_position())

		# cache selected city
		if isinstance(event, CitySelectedEvent):
			self.selected_unit_city = event.city

		# when map is loaded
		if isinstance(event, MapLoadedEvent):
			# cache loaded tilemap
			self._map = event.tilemap

		# on right click: unselect actual unit
		if isinstance(event, MouseRightClickedEvent):
			self.unselect_unit()

		# reset unit movement points before player starts
		if isinstance(event, NextOneEvent):
			actual_playernum = Locator.PLAYER_MGR.actual_player_num
			for unit in self.get_units_of_player(actual_playernum):
				unit.reset_mps()