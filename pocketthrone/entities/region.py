class Region:
	# parent city
	capital = None

	# name
	name = "No Man's Land"
	name_de = "Niemandland"

	# tiles
	tiles = []

	def __init__(self, capital, radius=3, name=None):
		self.capital = capital
		if name:
			self.name = name
		else:
			self.name = self.get_default_name()

	def get_default_name(self):
		capital_name = self.capital.get_name()
		return capital_namme + " Lands"
