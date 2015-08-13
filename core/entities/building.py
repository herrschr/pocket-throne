class Building:
	# engine properties
	_id = -1
	name = ""
	name_de = ""
	size = "1x1"

	# building type
	_type = None
	# possible building types & names
	_types = ["wall", "tower", "blacksmith", "bordel", "stables", "harbour", "tunnels", "siege_workshop", "mansion"]
	_names = {
		"wall": "Wall",
		"tower": "Tower",
		"blacksmith": "Blacksmith",
		"bordel": "Bordel",
		"stables": "Stables",
		"harbour": "Harbour",
		"tunnels": "Tunnel Systems",
		"siege_workshop": "Siege Workshop",
		"mansion": "Mansion"}

	# file paths
	image_override = None
	json_path = None

	# building flags (mainly for wonders)
	is_undestroyable = False
	is_owned_by_nature = False
	has_player_max = False
	has_map_max = False
	max_per_player = -1
	may_per_map = -1

	# changeable building vars
	city = None
	playerId = -1
	hp = -1

	# position as absolute and relative to town center
	pos_x = -1
	pos_y = -1
	rel_x = None
	rel_y = None

	def __init__(self, city, building_type):
		# abort when building_type is not defined
		if not building_type in self._types:
			print("[Building] type " + building_type +" is not defined")
			return
		# set building type & parent city
		self._type = building_type
		self.city = city

	# return the image file name of this building
	def get_image_path(self):
		if self.image_override:
			return self.image_override
		else:
			return "city_" + building_type + ".png"

	# returns the type (basename) of this building
	def get_type(self):
		return self._type

	# return the english name of this building
	def get_name(self):
		building_name = self._names[self.get_type()]
		return building_name

	# returns the parent city
	def get_city(self):
		return self.city

	# set the absolute position of this building
	def set_position(self, (pos_x, pos_y)):
		# set absolute position
		self.pos_x = pos_x
		self.pos_y = pos_y
		# calculate & set relative position
		city_pos = self.city.get_position()
		self.rel_x = city_pos[0] - pos_x
		self.rel_y = city_pos[1] - pos_y

	# set the relative position of this building towards it city
	def set_relative_position(self, (rel_x, rel_y)):
		# set relative position
		self.rel_x = rel_x
		self.rel_y = rel_y
		# calculate & set absolute position
		city_pos = self.city.get_position()
		self.pos_x = city_pos[0] + pos_x
		self.pos_y = city_pos[1] + pos_y

	# get the absulute position of this image
	def get_position(self):
		return (self.pos_x, self.pos_y)

	def get_relative_position(self):
		return (self.rel_x, self.rel_y)


