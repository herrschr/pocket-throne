from core.gui.widget import Widget
from core.gui import *
class Panel(Widget):
	widgets = []
	anchor = None
	align = None
	anchor = PANEL_ANCHOR_NOT_SET
	layout = {
		"left": -1,
		"top": -1,
		"width": -1,
		"height": -1
	}

	def __init__(self, eventmanager, panel_anchor):
		Widget.__init__(self, eventmanager)
	 	# set anchor and alignment
		self.anchor = panel_anchor
		# top or bottom panel: horizontal alignment
		if panel_anchor == PANEL_ANCHOR_TOP or panel_anchor == PANEL_ANCHOR_BOTTOM:
			self.align = PANEL_ALIGN_HORIZONTAL
		# side panels: vertical alignment
		elif panel_anchor == PANEL_ANCHOR_LEFT or panel_anchor == PANEL_ANCHOR_RIGHT:
	 		self.align = PANEL_ALIGN_VERTICAL

	def add_widget(self, to_add):
		self.widgets.append(to_add)

	def update(self):
		if not self.dirty:
			return
		# draw panel

	def __repr__(self):
		return "<Panel anchor=" + str(self.anchor) + ">"
