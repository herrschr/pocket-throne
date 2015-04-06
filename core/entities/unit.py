# Unit class for std-units and heroes
class Unit(object):
	# static unit vars, defaults
	_id = -1
	_instanciated = False

	name = ""
	name_de = ""
	categories = []
	image_path = None
	json_path = None
	health = 4
	movement = 2
	is_owned_by_nature = False
	weapon = None

	has_player_max = False
	has_map_max = False
	max_per_player = -1
	max_per_map = -1

	# changeable building vars
	player_num = -1
	hp = -1
	mp = movement
	pos_x = -1
	pos_y = -1

	def __init__(self, unit_name):
		self.name = unit_name

	def __repr__(self):
		return "<"  + self.name + " x=" + str(self.pos_x) + " y=" + str(self.pos_y) + ">"

	# load values from json skeleton
	def loadFromJson(json_path):
		pass

	# set the weapon of this uni
	def give_weapon(self, weapon):
		self.weapon = weapon

	def _id(self):
		if self._id != -1:
			return self._id
		else:
			return None

# Weapon class for std-unit or hero, defines the dealed damage, defined in <unit>.weapon
class Weapon(object):
	_id = -1
	name = ""
	name_de = ""
	value = 1
	distance = 1
	atk_vs_category = []
	image_path = None



