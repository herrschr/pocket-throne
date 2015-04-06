from core.gui.panel import Panel
from core.gui import *
from core.entities.event import *

class GuiManager:
	panels = []
	panel_at = {}

	def __init__(self, eventmanager):
		print ("guimgr: init with " + str(eventmanager))
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)
		self.gamestate = GAMESTATE_LOADING

	def add_panel(self, panel):
		# add pannel to collections
		anchor = panel.anchor
		self.panel_at[anchor] = panel
		self.panels = panel
		# fire GuiPanelAddedEvent
		ev_panel_added = GuiPanelAddedEvent(anchor, panel)
		self._eventmgr.post(ev_panel_added)

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
			self.add_panel(bottom_panel)

