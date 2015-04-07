from core.gui.widget import Widget
from core.gui import *

class Panel(Widget):
	widgets = []
	anchor = None
	align = None
	anchor = PANEL_ANCHOR_NOT_SET
	padding = 8
	color = (198, 172, 136)

	def __init__(self, eventmanager, panel_anchor):
		Widget.__init__(self, eventmanager)
	 	# set anchor and alignment
		self.anchor = panel_anchor
		# top or bottom panel: horizontal alignment
		if panel_anchor == PANEL_ANCHOR_TOP or panel_anchor == PANEL_ANCHOR_BOTTOM:
			self.align = PANEL_ALIGN_HORIZONTAL
			self.layout["left"] = 0
			self.layout["height"] = 64
		# side panels: vertical alignment
		elif panel_anchor == PANEL_ANCHOR_LEFT or panel_anchor == PANEL_ANCHOR_RIGHT:
	 		self.align = PANEL_ALIGN_VERTICAL

	def add_widget(self, to_add):
		widget_num = len(self.widgets)
		if self.align == PANEL_ALIGN_HORIZONTAL:
			# add padding to left and top
			to_add.layout["left"] = (self.layout["left"] + self.padding)
			to_add.layout["top"] = (self.layout["top"] + self.padding)
		to_add.parent = self
		self.widgets.append(to_add)

	def __repr__(self):
		return "<Panel anchor=" + str(self.anchor) + " widgets=" + str(len(self.widgets))+ ">"
