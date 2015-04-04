import os
import json
from core.entities.unit import Unit
from core.managers.filemanager import FileManager

class UnitManager:
	# Unit class skeleton (without mp, positions and _id)
	_skeletons = {}
	# Unit class array for instanciated units
	_units = []
	_last_unit_id = -1

	def __init__(self, mod_name):
		# ignore the mod name, no active modding system
		self.load_unit_skeletons("base")

	# returns a new, unused unit id
	def next_unit_id(self):
		self._last_unit_id += 1
		return self._last_unit_id

	# load unit skeletons from mods/<mod_name>/units/*.json
	def load_unit_skeletons(self, mod_name):
		unit_folder_path = FileManager.mod_path() + mod_name + "/units/"
		for file in os.listdir(unit_folder_path):
			if file.endswith(".json"):
				# load json file
				unit_basename = file.split(".")[0]
				unit_file = open(unit_folder_path + file)
				unit_json = json.loads(unit_file.read())
				unit_file.close()
				# load skeleton Unit from json and add it skeleton list
				unit = self.load_unit_skeleton(unit_json)
				self._skeletons[unit_basename] = unit

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

		# load maximal count per player
		max_per_player = unit_json["max_per_player"]
		if (max_per_player == -1):
			unit.has_player_max = False
			unit.max_per_player = -1
		else:
			unit.has_player_max = True
			unit.max_per_player = max_per_player

		# load maximal count on the whole map
		max_per_map = unit_json["max_per_map"]
		if (max_per_map == -1):
			unit.has_map_max = False
			unit.max_per_map = -1
		else:
			unit.has_map_max = True
			unit.max_per_map = max_per_map

		return unit

		def spawn_unit_at(self, unit_basename, (pos_x, pos_y)):
			pass

