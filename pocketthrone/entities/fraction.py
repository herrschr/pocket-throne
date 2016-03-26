from random import choice

class Fraction:
	# engine properties
	basename = None
	name = ""
	name_de = ""
	image_path = None

	city_prefixes = None
	city_postfixes = None

	def __init__(self, fraction_name):
		self.basename = fraction_name

	def get_name(self):
		'''returns the name of this fraction'''
		return self.name

	def get_basename(self):
		'''returns the basename of this fraction'''
		return self.basename

	def get_random_city_name(self):
		'''returns a random city name for this fraction'''
		# select a random pre- & postfix
		prefix = choice(self.city_prefixes)
		postfix = choice(self.city_postfixes)
		# sum them together & return city name
		city_name = prefix + postfix
		return city_name

	def get_image(self):
		prefix = "fraction_"
		file_name = prefix + self.basename
		return file_name

	def __repr__(self):
		'''returns an xml like representation of this fraction'''
		return "<Fraction name=" + self.name + ">"
