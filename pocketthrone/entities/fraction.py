from random import choice

class Fraction:
	# engine properties
	_basename = None
	name = ""
	name_de = ""
	banner_image_path = None

	city_prefixes = None
	city_postfixes = None

	def __init__(self, fraction_name):
		self._basename = fraction_name

	# returns the name of this fraction
	def get_name(self):
		return self.name

	# returns a random city name for this fraction
	def get_random_city_name(self):
		# select a random pre- & postfix
		prefix = choice(self.city_prefixes)
		postfix = choice(self.city_postfixes)
		# sum them together & return city name
		city_name = prefix + postfix
		return city_name

	def __repr__(self):
		return "<Fraction name=" + self.name + ">"