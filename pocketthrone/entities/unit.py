from pocketthrone.entities.enum import UnitType, UnitCategory, SkillLevel
from pocketthrone.entities.weapon import Weapon

# Unit class for std-units and heroes
class Unit:
	# system properties
	_id = -1
	basename = None
	_instanciated = False
	_possible_moves = []

	# engine properties
	name = ""
	name_de = ""
	image_path = None
	image_override = None

	# unit properties
	city = None
	health = 4
	movement = 2

	# unit's weapon
	weapon = None

	# unit category & type
	category = UnitCategory.UNITCAT_INFANTRY
	unit_type = UnitType.UNITTYPE_SOLIDER

	# unit flags
	is_disabled = False
	is_owned_by_nature = False
	max_per_player = -1
	max_per_map = -1

	# requirements
	requirements = []
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
		self.basename = unit_type

	def __repr__(self):
		'''returns an xml like representation of this unit'''
		return "<Unit player="  + str(self.player_num) + " type=" + self.name + \
			" pos=" + str(self.get_position()) + " hp=" + str(self.hp) + " mp=" + \
			str(self.mp) + ">"

	# load values from json skeleton
	def loadFromJson(json_path):
		pass

	def get_name(self):
		'''returns the english name of this unit'''
		return self.name

	def get_basename(self):
		'''returns the type (basename) of this unit'''
		return self.basename

	def get_type(self):
		'''returns unit type'''
		return self.unit_type

	def give_weapon(self, weapon):
		'''gives the unit a weapon object'''
		self.weapon = weapon

	def _id(self):
		'''returns unit id'''
		if self._id != -1:
			return self._id
		else:
			return None

	def get_player_num(self):
		'''returns number of the owner of this unit'''
		return self.player_num

	def get_player(self):
		'''returns owner of this unit'''
		return None

	def set_position(self, (pos_x, pos_y)):
		'''sets absolute unit position'''
		self.pos_x = pos_x
		self.pos_y = pos_y

	def get_position(self):
		'''returns absolute unit position'''
		return (self.pos_x, self.pos_y)

	def get_required_fraction(self):
		'''returns the basename of the required fraction of this unit or None'''
		return self.required_fraction

	def get_required_building(self):
		'''returns required building for unit recruition in a city or None'''
		return self.required_building

	def reset_mps(self):
		'''reset mp on turn change'''
		self.mp = self.movement

	def damage(self, damage):
		'''damages this unit (decrease hp)'''
		self.hp = self.hp - damage

	def heal(self, heal_hp):
		'''heal this unit (increase hp)'''
		self.hp = self.hp + heal_hp

	def get_image_path(self):
		'''returns path of image file of this units texture'''
		if self.image_override != None:
			return self.image_override
		return "unit_" + self.get_basename()

	def get_category(self):
		'''returns category of this unit'''
		return self.category
