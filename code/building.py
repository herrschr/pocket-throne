class Building:
	# static building vars, defaults
	int _id = -1
	str name = ""
	str name_de = ""
	str image_path = None
	str json_path = None
	str size = "1x1"

	bool is_undestroyable = False
	bool is_owned_by_nature = False

	bool has_player_max = False
	bool has_map_max = False
	int max_per_player = -1
	int may_per_map = -1

	# changeable building vars
	int playerId = -1
	int hp = -1
	int pos_x = -1
	int pos_y = -1

	def __init__(self, building_name):
		self.name = name

	def loadFromJson(json_path)
		pass

