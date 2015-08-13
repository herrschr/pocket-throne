class Building:
	# engine properties
	_id = -1
	_type = None
	name = ""
	name_de = ""
	size = "1x1"

	# file paths
	image_path = None
	image_override = None
	json_path = None

	# building flags
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
		self._type = building_type
		self.city = city
		self.image_path = "city_" + building_type + ".png"

	def loadFromJson(json_path):
		pass

	# get name of the image of this building
	def get_image_path(self):
		if self.image_override:
			return self.image_override
		else:
			return self.image_path

	# set the parent city
	def set_city(self, city):
		self.city = city

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


