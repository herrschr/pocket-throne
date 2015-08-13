import os
import json
import copy
from random import randrange
from core.entities.player import Player
from core.entities.fraction import Fraction
from core.entities.event import *
from core.managers.filemanager import FileManager
from core.managers.eventmanager import EventManager

# Manager class for players & turn methods
class PlayerManager:
	_tag = "[PlayerManager] "

	#game
	_mod_name = "base"

	# turn
	actual_turn = 0
	actual_player = None
	actual_player_num = -1

	# player
	players = []
	fractions = []

	_last_player_id = -1

	# add nature player (num=0) on the beginning
	def __init__(self, mod="base"):
		#register in EventManager
		EventManager.register_listener(self)

		# load mod &  fractions
		self.load_fractions(mod)

		# create nature player
		nature = Player()
		nature.name = "Nature"
		nature.color = (0, 0, 0)
		self._add_player(nature)

	# set the mod for the actual game
	def set_mod(self, mod_name):
		self._mod_name = mod_name

	# get the name of actual setted mod
	def get_mod_name(self):
		return self._mod_name

	# start the game with turn 1
	def start_game(self):
		# set turn=0 and player=1
		self.actual_turn = 0
		actual_player_num = 1
		self.change_actual_player(1)

	# load all fractions from mods/<modname>/fractions/*.json files
	def load_fractions(self, mod_name):
		fraction_folder_path = FileManager.mod_path() + mod_name + "/fractions/"
		for file in os.listdir(fraction_folder_path):
			if file.endswith(".json"):
				# load the fraction file content to fraction_json
				fraction_basename = file.split(".")[0]
				fraction_file_path = fraction_folder_path + file
				fraction_filecontent = FileManager.read_file(fraction_file_path)
				if fraction_filecontent != "":
					fraction_json = json.loads(fraction_filecontent)
					# create the fraction object from json
					fraction = Fraction()
					fraction._basename = fraction_basename
					fraction.name = fraction_json["name"]
					fraction.name_de = fraction_json["name_de"]
					fraction.city_prefixes = fraction_json["city_prefixes"]
					fraction.city_postfixes = fraction_json["city_postfixes"]
					# add fraction to the array
					self.fractions.append(fraction)
		print("[IngameManager] fractions=" + repr(self.fractions))

	# add a player by class
	def _add_player(self, player, fraction=None):
		# add player number to player and add all to player list
		new_player = player
		new_player.num = self.next_player_number()
		self.players.append(new_player)
		# debug: log player addition
		print (self._tag + "added player name=" + new_player.name + " on number " + str(new_player.num))

	# add a new player by name and color
	def add_new_player(self, player_name, (r, g, b), fraction_name=None):
		new_player = Player()
		new_player.name = player_name
		new_player.color = (r, g, b)
		if fraction_name != None:
			new_player.fraction = self.get_fraction_by_name(fraction_name)
		else:
			new_player.fraction = self.get_random_fraction()
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
			if fraction.name == fraction_name:
				return fraction

	# return a random fraction
	def get_random_fraction(self):
		i = randrange(0, len(self.fractions) -1, 1)
		return self.fractions[i]

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
		if isinstance(event, GameStartedEvent):
			self.start_game()

		if isinstance(event, MouseClickedEvent):
			pass

		if isinstance(event, GuiButtonClickedEvent):
			if event.button_tag == "NEXTTURN":
				self.forward()