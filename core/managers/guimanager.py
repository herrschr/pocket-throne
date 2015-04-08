from core.gui.panel import Panel
from core.gui.labelwidget import LabelWidget
from core.gui.multilinelabelwidget import MultiLineLabelWidget
from core.gui import *
from core.entities.event import *

class GuiManager:
	panels = []
	panel_at = {}
	_last_panel_id = -1

	def __init__(self, eventmanager):
		print ("guimgr: init with " + str(eventmanager))
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)
		self.gamestate = GAMESTATE_LOADING

	# returns a new gui panel id
	def next_panel_id(self):
		self._last_panel_id += 1
		return self._last_panel_id

	def add_panel(self, panel):
		# add panel to collections
		anchor = panel.anchor
		panel._id = self.next_panel_id()
		self.panel_at[panel.anchor] = panel
		self.panels = panel
		# fire GuiPanelAddedEvent
		ev_panel_added = GuiPanelAddedEvent(anchor, panel)
		self._eventmgr.fire(ev_panel_added)

	def click_in_gui(self, (click_x, click_y)):
		for panel in self.panels:
			pass

	def click_in_panel(self, (click_x, click_y)):
		pass

	def on_event(self, event):
		# add ingame panels when map is loaded
		if isinstance(event, GameStartedEvent):
			# switch in INGAME state
			self.gamestate = GAMESTATE_INGAME
			# add bottom panel
			bottom_panel = Panel(self._eventmgr, PANEL_ANCHOR_BOTTOM)
			# add heading label
			h_label = MultiLineLabelWidget(self._eventmgr)
			h_label.set_line(0, "No Selection..")
			# add data label
			# data_label = LabelWidget(self._eventmgr)
			# data_label.set_text("nodata")
			# add them to panel and add panel to GuiManager
			bottom_panel.add_widget(h_label)
			# bottom_panel.add_widget(data_label)
			self.add_panel(bottom_panel)

		# when a unit is selected, show unit's name on label1
		if isinstance(event, UnitSelectedEvent):
			selected_unit = event.unit
			selected_label = self.panel_at[PANEL_ANCHOR_BOTTOM].widgets[0]
			selected_label.set_line(1, "Unit: " + selected_unit.name)
			selected_label.set_line(2, "HP: " + str(selected_unit.hp) + " | MP: " + str(selected_unit.mp))

		# when a unit is unselected, hide label1
		if isinstance(event, UnitUnselectedEvent):
			selected_label = self.panel_at[PANEL_ANCHOR_BOTTOM].widgets[0]
			selected_label.set_line(1, "")
			selected_label.set_line(2, "")