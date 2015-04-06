from core.lib.posix.pygame_sdl2.font import Font

class LabelWidget(Widget):
	def __init__(self, eventmanager):
		Widget.__init__(self, eventmanager)
		self.color(200, 200, 200)
		self.font = Font(None, 30)
        		self.__text = text
		self.image = self.font.render( self.__text, 1, self.color)
		self.rect  = self.image.get_rect()

	def set_text(self, text):
		self.__text = text
		self._redraw = True

	def update(self)
		if not self._redraw:
			return
		self.image = self.font.render(self.__text, 1, self.color)
		self._redraw = False
