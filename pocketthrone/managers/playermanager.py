import os
import json
import copy
from random import choice

from pocketthrone.entities.enum import WidgetAction
from pocketthrone.entities.player import Player
from pocketthrone.entities.fraction import Fraction
from pocketthrone.entities.event import *
from pocketthrone.managers.locator import Locator
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.eventmanager import EventManager

# Manager class for players & turn methods
class PlayerManager:
	# engine properties
	_tag = "[PlayerManager] "

	# turn related properties
	actual_turn = 0
	actual_player = None
	actual_player_num = -1

	# player related properties
	_last_player_id = -1
	players = []
	fractions = []

	# add nature player (num=0) on the beginning
	def __init__(self):
		#register in EventManager
		EventManager.register_listener(self)
		# load fractions into PlayerManager
		selected_mod = Locator.MOD_MGR.get_selected_mod()
		self.load_fractions(selected_mod._basename)
		# create nature player
		nature = Player()
		nature.name = "Nature"
		nature.color = (0, 0, 0)
		self._add_player(nature)

	def fill_tilemap_players(self, tilemap):
		for player in tilemap.players:
			self._add_player(player)

	# start the game with turn 1
	def start_game(self):
		# set turn=0 and player=1
		self.actual_turn = 0
		actual_player_num = 1
		self.change_actual_player(1)

	# load all fractions from mods/<modname>/fractions/*.json files
	def load_fractions(self, mod_name):
		mod_name = Locator.MOD_MGR.get_selected_mod()._basename
		fraction_folder_path = FileManager.mod_path() + mod_name + "/fractions/"
		for file in os.listdir(fraction_folder_path):
			if file.endswith(".json"):
				# load the fraction file content into fraction_json object
				fraction_basename = file.split(".")[0]
				fraction_file_path = fraction_folder_path + file
				fraction_filecontent = FileManager.read_file(fraction_file_path)
				# when the file isn't empty, start creating the object
				if fraction_filecontent != "":
					# create json object and fraction entity
					fraction_json = json.loads(fraction_filecontent)
					fraction = Fraction(fraction_basename)
					# fill fractions properties from json
					fraction.name = fraction_json["name"]
					fraction.name_de = fraction_json["name_de"]
					fraction.city_prefixes = fraction_json["city_prefixes"]
					fraction.city_postfixes = fraction_json["city_postfixes"]
					# add fraction to the array
					self.fractions.append(fraction)
		print("[IngameManager] fractions=" + repr(self.fractions))

	# returns all players
	def get_players(self):
		return self.players

	# add a player by class, system method
	def _add_player(self, player, fraction=None):
		# add player number to player and add all to player list
		new_player = player
		new_player.num = self.next_player_number()
		# set player fraction
		if not fraction and not new_player.fraction:
			new_player.fraction = self.get_random_fraction()
		elif fraction and not new_player.fraction:
			new_player.fraction = self.get_fraction_by_name(fraction)
		# add new player to player list
		self.players.append(new_player)
		print (self._tag + "added player name=" + new_player.name + " on number " + str(new_player.num))


	# add a new player by name and color
	def add_new_player(self, player_name, (r, g, b), fraction_name=None):
		new_player = Player()
		new_player.name = player_name
		new_player.color = (r, g, b)
		# when a specific fraction is wanted: set it
		if fraction_name != None:
			new_player.fraction = self.get_fraction_by_name(fraction_name)
		# when no specific fraction is wanted: select random fraction
		else:
			new_player.fraction = self.get_random_fraction()
		# add player by class in PlayerManager
		self._add_player(new_player)

	# get a player by its number
	def get_player_by_num(self, player_num):
		for player in self.players:
			if player.get_number() == player_num:
				return player
		return None

	# next turn & change player to player_num
	def change_actual_player(self, player_num):
		# update player
		self.actual_player_num = player_num
		self.actual_player = self.players[player_num]
		# fire NextOneEvent
		ev_nextone = NextOneEvent(self.actual_player)
		EventManager.fire(ev_nextone)

	# return a fraction by its name
	def get_fraction_by_name(self, fraction_name):
		for fraction in self.fractions:
			if fraction._basename == fraction_name:
				return fraction

	# return a random fraction
	def get_random_fraction(self):
		return choice(self.fractions)

	# internal: end turn and start a next one
	def next_turn(self):
		# next turn
		self.actual_turn += 1
		# trigger NextTurnEvent
		ev_nextturn = NextTurnEvent(self.actual_turn)
		EventManager.fire(ev_nextturn)
		# player one starts
		actual_player_num = 1
		self.change_actual_player(actual_player_num)

	# add player income per city for each one
	def _add_income_for_cities(self):
		for player in self.get_players():
			# calculate the gold gain depending on city count of the player
			player_cities = Locator.CITY_MGR.get_cities(for_specific_player=player.get_number())
			city_count = len(player_cities)
			# 5 gold per city per turn
			gold_gain = city_count *5
			# add it to the players gold treasure
			player.gain_gold(gold_gain)

	# internal: end turn of the actual player and switch to next one
	def next_one(self):
		# next player
		actual_player_num = self.actual_player_num + 1
		self.change_actual_player(actual_player_num)

	# switch player or update turn, "End Turn" button beheaviour
	def forward(self):
		player_count = len(self.players) -1
		# player isn't the last one
		if player_count - self.actual_player_num > 0:
			self.next_one()
		# player is the last one this turn
		elif player_count - self.actual_player_num  == 0:
			self.next_turn()

	# internal: get next player number
	def next_player_number(self):
		self._last_player_id += 1
		return self._last_player_id

	def on_event(self, event):
		# on MapLoadedEvent: add tilemap players to holder list
		if isinstance(event, MapLoadedEvent):
			map_players = event.tilemap.players
			for player in map_players:
				# set player fraction entity
				player_fraction_name = player._fraction_name
				self._add_player(player, fraction=player_fraction_name)

		# on GameStartedEvent: start game with first turn
		if isinstance(event, GameStartedEvent):
			self.start_game()

		# on NextTurnEvent: add income per city for each player
		if isinstance(event, NextTurnEvent):
			self._add_income_for_cities()

		# on button click: forward players
		if isinstance(event, GuiButtonClickedEvent):
			if event.action == WidgetAction.ACTION_NEXTTURN:
				self.forward()