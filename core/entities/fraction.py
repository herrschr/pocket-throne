class Fraction:
	# engine properties
	_basename = None
	name = ""
	name_de = ""
	banner_image_path = None

	city_prefixes = None
	city_postfixes = None

	def __init__(self):
		pass

	# returns the name of this fraction
	def get_name(self):
		return self.name

	# returns a random city name for this fraction
	def get_random_city_name(self):
		prefix_rnd = randrange(0, len(self.city_prefixes) -1, 1)
		postfix_rnd = randrange(0, len(self.city_postfixes) -1, 1)

		city_name = self.city_prefixes[prefix_rnd] + self.city_postfixes[postfix_rnd]
		return city_name

	def __repr__(self):
		return "<Fraction name=" + self.name + ">"