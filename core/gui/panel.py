from core.gui.widget import Widget
from core.gui import *
from core.entities.event import *

class Panel:
	_id = -1
	_placed = False
	_usedspace = 0
	_last_widget_pos = -1
	widgets = []
	anchor = None
	align = None
	anchor = PANEL_ANCHOR_NOT_SET
	padding = 8
	color = (198, 172, 136)

	layout_override = False
	layout = {
		"left": 0,
		"top": 0,
		"width": 0,
		"height": 0
	}

	def __init__(self, eventmanager, panel_anchor):
		# register in eventmanager
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)
		self.dirty = True
	 	# set anchor and alignment
		self.anchor = panel_anchor
		# top or bottom panel: horizontal alignment
		if panel_anchor == PANEL_ANCHOR_TOP or panel_anchor == PANEL_ANCHOR_BOTTOM:
			self.align = PANEL_ALIGN_HORIZONTAL
			self.left = 0
			self.top = None
			self.width = None
			self.height= 64
		# side panels: vertical alignment
		elif panel_anchor == PANEL_ANCHOR_LEFT or panel_anchor == PANEL_ANCHOR_RIGHT:
	 		self.align = PANEL_ALIGN_VERTICALwidget

	 # returns a new, unused unit id
	def next_widget_pos(self):
		self._last_widget_pos += 1
		return self._last_widget_pos

	def get_layout(self):
		return (self.left, self.top, self.width, self.height)

	def update_widget(self, new_widget):
		widget_pos_in_panel = new_widget._pos_in_panel
		old_widget = self.get_nth_widget(widget_pos_in_panel)
		self.widgets.remove(old_widget)
		self.widgets.append(new_widget)
		print "old widget:" + str(old_widget)
		print "new widget" + str(new_widget)

	def get_widget_by_id(self, widget_id):
		for widget in self.widgets:
			if widget_id == widget._id:
				return widget
		return None

	def get_nth_widget(self, pos_in_panel):
		for widget in self.widgets:
			if pos_in_panel == widget._pos_in_panel:
				return widget
		return None


	def set_layout(self, (left, top, width, height)):
		if left:
			self.left = left
		if top:
			self.top = top
		if width:
			self.width = width
		if height:
			self.height = height

	def add_widget(self, to_add):
		widget_num = len(self.widgets)
		if self.align == PANEL_ALIGN_HORIZONTAL:
			print("add widget " + str(to_add.__class__) + " at " + str(to_add.get_layout()))
		to_add._pos_in_panel = self.next_widget_pos()
		to_add.parent = self
		self.widgets.append(to_add)

	# align widgets in panel after it's placed
	def align_widgets(self, panel_align):
		aligned_widgets = []
		# for horizontal panels
		if panel_align == PANEL_ALIGN_HORIZONTAL:
			widget_number = 0
			# add padding on x before adding a widget
			self._usedspace = self.padding
			while widget_number < len(self.widgets):
				to_align = self.widgets[widget_number]
				# only align non-free placed widgets (layout_override = Flase)
				if to_align.layout_override == True:
					continue
				# fixed y pos; x increases per widget
				widget_left = self._usedspace
				widget_top = self.top + self.padding
				to_align.left = widget_left
				to_align.top = widget_top
				# increase x position; process next widget
				self._usedspace += to_align.width
				widget_number += 1

	def __repr__(self):
		return "<Panel _id=" + str(self._id) + " anchor=" + str(self.anchor) + " widgets=" + str(len(self.widgets)) + \
			" layout=" + str(self.get_layout()) + ">"

	def on_event(self, event):
		# on panel update
		if isinstance(event, GuiPanelUpdatedEvent):
			# when panel is placed: align all widgets
			if event.panel._id == self._id and event.action == "placed":
				self.align_widgets(self.align)
				self._placed = True

