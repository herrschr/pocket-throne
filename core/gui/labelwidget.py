from pygame_sdl2.font import Font
from core.gui.widget import Widget

class LabelWidget(Widget):
	color = (0, 0, 0)

	def __init__(self, eventmanager):
		Widget.__init__(self, eventmanager)
		# render Widget's image
		self.font = Font(None, 30)
		self.__text = "Loading ..."
		self.image = self.font.render(self.__text, 1, self.color)
		# update size; trigger reload
		self._update_size()

	def set_text(self, to_set):
		# change text
		self.__text = to_set
		# set new widget size
		self._update_size()
		self.trigger_redraw()

	def get_text(self):
		return self.__text

	def _update_size(self):
		rect = self.image.get_rect()
		self.set_layout((None, None, rect.width, rect.height))

	def update(self):
		if not self.dirty:
			return
		self.image = self.font.render(self.__text, 1, self.color)
		self.dirty = False

	def __repr__(self):
		return "<LabelWidget panel=" + str(self.parent.anchor) + " text=" + self.__text + " layout=" + str(self.get_layout()) + ">"
