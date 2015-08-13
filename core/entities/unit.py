# Unit class for std-units and heroes
class Unit(object):
	# system properties
	_id = -1
	_basename = None
	_instanciated = False
	_possible_moves = []

	# engine properties
	_name = ""
	name = ""
	name_de = ""
	image_path = None

	# constants
	categories = []
	health = 4
	movement = 2
	is_owned_by_nature = False
	weapon = None

	# limited number
	has_player_max = False
	has_map_max = False
	max_per_player = -1
	max_per_map = -1

	# TODO: load requirements and costs into skeletons
	# requirements
	required_building = None
	required_fraction = None

	# costs
	cost_turns = 5
	cost_gold = 10

	# changeable building vars
	player_num = -1
	hp = -1
	mp = movement

	# position
	pos_x = -1
	pos_y = -1

	# experience level
	experience = 0

	def __init__(self, unit_name):
		self.name = unit_name

	def __repr__(self):
		return "<Unit player="  + str(self.player_num) + " type=" + self.name + \
			" pos=" + str(self.get_position()) + " hp=" + str(self.hp) + " mp=" + \
			str(self.mp) + ">"

	# load values from json skeleton
	def loadFromJson(json_path):
		pass

	def get_name(self):
		return self.name

	# set the weapon of this uni
	def give_weapon(self, weapon):
		self.weapon = weapon

	# get unit id
	def _id(self):
		if self._id != -1:
			return self._id
		else:
			return None

	# set unit position with tuple (x, y)
	def set_position(self, (pos_x, pos_y)):
		self.pos_x = pos_x
		self.pos_y = pos_y

	# get unit position tuple (x, y)
	def get_position(self):
		return (self.pos_x, self.pos_y)

	# reset mp on turn change
	def reset_mps(self):
		self.mp = self.movement

	# damage this unit (decrease hp)
	def damage(self, damage):
		self.hp = self.hp - damage

	# heal this unit (increase hp)
	def heal(self, heal_hp):
		self.hp = self.hp + heal_hp

# Weapon class for std-unit or hero, defines the dealed damage, defined in <unit>.weapon
class Weapon(object):
	# engine properties
	_id = -1
	name = ""
	name_de = ""
	image_path = None

	# constants
	value = 1
	distance = 1
	hit_percent = 75
	atk_vs_category = []



