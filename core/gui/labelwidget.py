from core.lib.posix.pygame_sdl2.font import Font
from core.gui.widget import Widget

class LabelWidget(Widget):
	color = (0, 0, 0)

	def __init__(self, eventmanager):
		Widget.__init__(self, eventmanager)
		# self.color(200, 200, 200)
		self.font = Font(None, 30)
		self.__text = "Loading ..."
		self.image = self.font.render(self.__text, 1, self.color)
		self.rect  = self.image.get_rect()

	def set_text(self, to_set):
		self.__text = to_set
		self.trigger_redraw()

	def get_text(self):
		return self.__text

	def update(self):
		if not self.dirty:
			return
		self.image = self.font.render(self.__text, 1, self.color)
		self.dirty = False

	def __repr__(self):
		return "<LabelWidget panel=" + str(self.parent.anchor) + " text=" + self.__text + ">"
