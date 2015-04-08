from pygame_sdl2.font import Font
from pygame_sdl2 import Surface
from pygame_sdl2 import *
from core.gui.widget import Widget

class MultiLineLabelWidget(Widget):
	color = (0, 0, 0)
	padding = 4

	def __init__(self, eventmanager):
		Widget.__init__(self, eventmanager)
		# render Widget's image
		self.font = Font(None, 30)
		self.__lines = ["", ""]
		self.image = None
		# render and set updated size
		self._render()
		self._update_size()

	# generate new self.image, drawn by PygameDrawingManager
	def _render(self):
		width = 0
		height = 0
		# generate real size for Surface creation
		for line in self.__lines:
			width = max(width, self.font.size(line)[0])
			height = height + 2 + self.font.get_linesize()
		# render each line on self.image
		self.image = Surface((width, height), SRCALPHA, 32)
		self.width = width
		self.height = height
		height = 0
		for line in self.__lines:
			if line != "" and line != None:
				line_img = self.font.render(line, 1, self.color)
				self.image.blit(line_img, (0, height))
			height += self.font.get_linesize()

	# set text of a line (starts at 1)
	def set_line(self, line_num, to_set):
		# change text
		self.__lines[line_num -1] = to_set
		# set new widget size
		self._render()
		self._update_size()
		self.trigger_redraw()

	# get text of a line (starts with 1)
	def get_line(self, line_num):
		return self.__line[line_num +1]

	def _update_size(self):
		rect = self.image.get_rect()
		self.set_layout((None, None, rect.width, rect.height))

	def update(self):
		if not self.dirty:
			return
		self._render()
		self.dirty = False

	def __repr__(self):
		return "<MultiLineLabelWidget panel=" + str(self.parent.anchor) + " lines=" + str(self.__lines) + " layout=" + str(self.get_layout()) + ">"
