class Player(object):
	num = -1
	name = "Anonymous"
	color = (255, 0, 0)

	fraction = None

	def __repr__(self):
		return "<Player num=" + str(self.num) + " name=" + self.name + " fraction=" + repr(self.fraction) + ">"

	def get_number(self):
		return self.num

	def get_name(self):
		return self.name

	def get_color(self):
		return self.color

	def get_fraction(self):
		return self.fraction