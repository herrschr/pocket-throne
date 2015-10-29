from core.entities.weapon import Weapon

# Unit class for std-units and heroes
class Unit(object):
	# system properties
	_id = -1
	_basename = None
	_instanciated = False
	_possible_moves = []

	# engine properties
	name = ""
	name_de = ""
	image_path = None

	# unit properties
	health = 4
	movement = 2

	# unit's weapon
	weapon = None

	# unit category (INF, HEAVY_INF, CAV, MACHINE)
	category = None
	# unit type (SOLDIER, MERC, GUARD, RIDDEN, KNIGHT)
	unit_type = None

	# unit flags
	is_disabled = False
	is_owned_by_nature = False
	max_per_player = -1
	max_per_map = -1

	# requirements
	required_building = None
	required_fraction = None

	# costs
	cost_turns = 5
	cost_gold = 10

	# unit's owner
	player_num = -1

	# changeable unit vaiables
	hp = -1
	mp = movement

	# position
	pos_x = -1
	pos_y = -1

	# experience level
	experience = 0

	def __init__(self, unit_type):
		self._basename = unit_type

	# returns an xml like representation of this unit
	def __repr__(self):
		return "<Unit player="  + str(self.player_num) + " type=" + self.name + \
			" pos=" + str(self.get_position()) + " hp=" + str(self.hp) + " mp=" + \
			str(self.mp) + ">"

	# load values from json skeleton
	def loadFromJson(json_path):
		pass

	# returns the english name of this unit
	def get_name(self):
		return self.name

	# returns the type (basename) of this unit
	def get_type(self):
		return self._basename

	# set the weapon of this uni
	def give_weapon(self, weapon):
		self.weapon = weapon

	# get unit id
	def _id(self):
		if self._id != -1:
			return self._id
		else:
			return None

	# returns the number of this units owner
	def get_player_num(self):
		return self.player_num

	# return the owner player class of this unit
	def get_player(self):
		return None

	# set unit position with tuple (x, y)
	def set_position(self, (pos_x, pos_y)):
		self.pos_x = pos_x
		self.pos_y = pos_y

	# get unit position tuple (x, y)
	def get_position(self):
		return (self.pos_x, self.pos_y)

	# returns the basename of the required fraction of this unit or None
	def get_required_fraction(self):
		return self.required_fraction

	# get the required building for unit recruition in a city or None
	def get_required_building(self):
		return self.required_building

	# reset mp on turn change
	def reset_mps(self):
		self.mp = self.movement

	# damage this unit (decrease hp)
	def damage(self, damage):
		self.hp = self.hp - damage

	# heal this unit (increase hp)
	def heal(self, heal_hp):
		self.hp = self.hp + heal_hp



