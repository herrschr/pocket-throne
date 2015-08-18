class Player(object):
	# engine properties
	num = -1
	# static player properties
	name = "Anonymous"
	color = (255, 0, 0)
	fraction = None
	hero = None
	# changable player properties
	gold = 0
	# player properties for statistics
	killed_units = 0
	army_size = 0
	biggest_army_size = 0

	# returns an xml like representation of this player
	def __repr__(self):
		return "<Player num=" + str(self.num) + " name=" + self.name + " gold=" + str(self.gold) + " fraction=" + repr(self.fraction) + ">"

	# returns the player number
	def get_number(self):
		return self.num

	# returns the name of this player
	def get_name(self):
		return self.name

	# returns the RGB color tuple of this player
	def get_color(self):
		return self.color

	# returns the fraction entity of this player
	def get_fraction(self):
		return self.fraction

	# returns the gold treasure of this player
	def get_gold(self):
		return self.gold

	# increase gold of this player by gold_gain
	def gain_gold(self, gold_gain):
		self.gold += gold_gain

	# decrease gold of this player by gold_costs
	def reduce_gold(self, gold_costs):
		self.gold -= gold_costs