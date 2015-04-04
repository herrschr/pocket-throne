class Unit(object):
	# static unit vars, defaults
	_id = -1
	name = ""
	name_de = ""
	categories = []
	image_path = None
	json_path = None
	movement = 2
	is_owned_by_nature = False

	has_player_max = False
	has_map_max = False
	max_per_player = -1
	may_per_map = -1

	# changeable building vars
	playerId = -1
	hp = -1
	mp = movement
	pos_x = -1
	pos_y = -1
	weapon = None

	def __init__(self, unit_name):
		self.name = name
		self.categories.add("CAT_INF_MELEE")

	def loadFromJson(json_path):
		pass

	def give_weapon(weapon):
		self.weapon = weapon

class Weapon(object):
	_id = -1
	name = ""
	name_de = ""
	value = 1
	atk_vs_category = []
	image_path = None

	def __init__(self, weapon_name):
		self.name = weapon_name



