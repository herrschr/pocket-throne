class Player(object):
	num = -1
	name = "Anonymous"
	color = (255, 0, 0)

	def __repr__(self):
		return "<Player num=" + str(self.num) + " name=" + self.name + ">"