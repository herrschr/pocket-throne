class Building:
	# static building vars, defaults
	_id = -1
	name = ""
	name_de = ""
	image_path = None
	json_path = None
	size = "1x1"

	is_undestroyable = False
	is_owned_by_nature = False

	has_player_max = False
	has_map_max = False
	max_per_player = -1
	may_per_map = -1

	# changeable building vars
	playerId = -1
	hp = -1
	pos_x = -1
	pos_y = -1

	def __init__(self, building_name):
		self.name = building_name

	def loadFromJson(json_path):
		pass

	def set_position(self, (pos_x, pos_y)):
		self.pos_x = pos_x
		self.pos_y = pos_y

	def get_position(self):
		return (self.pos_x, self.pos_y)


