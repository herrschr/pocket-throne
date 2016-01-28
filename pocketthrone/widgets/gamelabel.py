__all__ = ('GameLabel')

from kivy.graphics import Rectangle, Color
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label

from pocketthrone.managers.locator import L
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.entities.event import *

class GameLabel(Label):
	_tag = "[GameLabel] "
	_dirty = True

	# text size weighting default
	_weight_mod = 1.0
	# default fontsize in px
	_std_fontsize = 12
	# default font color
	_std_fontcolor =  (0, 0, 0, 1)
	# CoreLabel kivy class for getting font texture
	_corelabel = None

	def __init__(self, link=None, weight=1, icon_source="none.png", **kwargs):
		# initialize widget
		super(GameLabel, self).__init__(**kwargs)
		EventManager.register(self)
		L.WidgetManager.register(link, self)
		# set initial GameLabel state
		self.link = link
		self.weight = weight
		self.font_color = self._std_fontcolor
		self.icon_source = L.RootDirectory + "img/" + icon_source
		self.halign = "left"
		self.valign = "top"

	# trigger a widget full redraw
	def trigger_redraw(self):
		self._dirty = True

	# update all neccessary stuff
	def update(self):
		if self._dirty:
			self.update_font()
			self.update_plaintext()
			self.update_layout()
		self._dirty = False

	# update font related calculations; use class variables!
	def update_font(self):
		# update weight & related font size
		calculated_weight = self._weight_mod *self.weight
		if not self.font_color:
			self.font_color = self._std_fontcolor

	# update layout data; use class variables!
	def update_layout(self):
		if not self._corelabel:
			# create new label
			corelabel = CoreLabel(text=self.text, font_size=self.font_size, color=self.font_color)
			corelabel.refresh();
			self._corelabel = corelabel
		labeltexture = self._corelabel.texture
		self.canvas.add(Rectangle(texture=labeltexture, size=(self.width, self.height)))

	# update text content; use class variables!
	def update_plaintext(self):
		if self.text == None:
			self.text = ""

	# get the GameLabels tag
	def get_label_tag(self):
		return self.label_tag

	# set the GameLabels tag
	def set_label_tag(self, value):
		self.label_tag = value
		self.trigger_redraw()

	# get the GameLabels weight (text size modifier)
	def get_weight(self):
		return self.weight

	# set the GameLabels weight (text size modifier)
	def set_weight(self, value):
		self.weight = value
		self.update()

	# set horizontal and vertical text alignment
	def set_aligns(self, halign, valign):
		self.halign = halign
		self.valign = valign

	# get tha absolute path to the icons Image source
	def get_icon_source(self):
		return self.icon_source

	# set the absolute path to the icons Image source
	def set_icon_source(self, value):
		self.icon_source = value
		self.update()

	# get the GameLabels text content as string
	def get_plaintext(self):
		return self.text

	# get_plaintext() alias
	def get_text(self):
		return self.get_plaintext()

	# set_plaintext(value) alias
	def set_text(self, value):
		self.set_plaintext(value)

	# set the GameLabels text content as string
	def set_plaintext(self, value):
		self.text = value
		self.trigger_redraw()

	# handles game-intern Events
	def on_event(self, event):
		if (isinstance(event, TickEvent)):
			self.update()
