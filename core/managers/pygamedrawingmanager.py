from pygame_sdl2 import *
from pygame_sdl2.rect import Rect
from core.entities.event import *
from core.managers.filemanager import FileManager
from core.gui import *

class PygameDrawingManager:
	def __init__(self, eventmanager):
		# register in EventManager
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)

		self._dirty_map = False
		self._dirty_menu = False

		self.tilemap = None
		self.selected_tile = None
		self.actual_turn = None
		self.actual_player = None

		self.screen_width = 1
		self.screen_height = 1

		self.panels = {}

		# initialize pygame_sdl2
		global screen
		pygame_sdl2.init()
		screen = pygame_sdl2.display.set_mode((self.screen_width, self.screen_height), RESIZABLE)
		screen.fill((255, 255, 255))
		pygame_sdl2.display.update()

	# resize string; new_size is a tuple
	def resize_display(self):
		global screen
		screen = pygame_sdl2.display.set_mode((self.screen_width, self.screen_height), RESIZABLE)
		screen.fill((255, 255, 255))
		pygame_sdl2.display.flip()

	def draw_map(self, tilemap):
		# draw tiles
		for tile in self.tilemap.tiles:
			# load image from Tile._image_path
			full_img_path = FileManager.image_path() + tile._image_path
			image = pygame_sdl2.image.load(full_img_path).convert()
			# calculate x and y position on screen and render tile image
			gui_position = self.mappos_to_gui((tile.pos_x, tile.pos_y))
			screen.blit(image, gui_position)

		# draw selected tile
		if (self.selected_tile):
			# load static selected-tile image (img/selected_tile.png)
			selected_img_path = FileManager.image_path() + "tile_selected.png"
			selected_img = pygame_sdl2.image.load(selected_img_path).convert_alpha()
			# calculate x and y position on screen and render selected tile image there
			selected_gui_pos = self.mappos_to_gui(self.selected_tile.get_position())
			screen.blit(selected_img, selected_gui_pos)

		# draw units
		for unit in tilemap.units:
			# load unit image from Unit.image_path
			full_img_path = FileManager.image_path() + unit.image_path
			image = pygame_sdl2.image.load(full_img_path).convert_alpha()
			# calculate x and y position on screen and render unit image there
			gui_position = self.mappos_to_gui((unit.pos_x, unit.pos_y))
			screen.blit(image, gui_position)

	def draw_menu(self):
		# for each existing panel
		for panel in self.panels.itervalues():
			# update dirty widgets
			if panel.dirty:
				print("panel-dirty")
				# redraw underlaying panel
				#panel_l = panel.layout["left"]
				panel_l = 0
				panel_t = panel.layout["top"]
				panel_w = panel.layout["width"]
				panel_h = panel.layout["height"]
				screen.fill(panel.color, rect=Rect(panel_l, panel_t, panel_w, panel_h))
				for widget in panel.widgets:
					if widget.dirty:
						print("widget-dirty")
						# draw updated widget overlay
						widget.update()
						gui_pos = (widget.layout["left"], widget.layout["top"])
						screen.blit(widget.image, gui_pos)

	# translates position on map grid in position on screen
	def mappos_to_gui(self,(x, y)):
		gui_x = x * self.tilemap.TILESIZE
		gui_y = y *self.tilemap.TILESIZE
		return (gui_x, gui_y)

	# translates position from screen into map grid position
	def gui_to_mappos(self, (x, y)):
		pos_x = int(x / self.tilemap.TILESIZE)
		pos_y = int(y / self.tilemap.TILESIZE)
		return (pos_x, pos_y)

	# event handling
	def on_event(self, event):
		# each tick
		if isinstance(event, TickEvent):
			# when tilemap != None & map data is updated: draw it
			if self.tilemap and self._dirty_map:
				self.draw_map(self.tilemap)
			# when menu is updated: draw
			if self._dirty_menu:
				self.draw_menu()
			# on any change: update display
			if self._dirty_map or self._dirty_menu:
				pygame_sdl2.display.flip()
			self._dirty_map = False
			self._dirty_menu = False

		# when map is loaded
		if isinstance(event, MapLoadedEvent):
			# load tilemap
			self.tilemap = event.tilemap
			# resize display to map size
			self.screen_width= self.tilemap.size_x * self.tilemap.TILESIZE
			self.screen_height = self.tilemap.size_y * self.tilemap.TILESIZE
			self.resize_display()
			self._dirty_map = True

		# when a tile is selected
		if isinstance(event, TileSelectedEvent):
			self.selected_tile = event.selected_tile
			self._dirty_map = True

		# when a tile is unselected
		if isinstance(event, TileUnselectedEvent):
			self.selected_tile = None
			self._dirty_map = True

		# when a panel is added in GUI
		if isinstance(event, GuiPanelAddedEvent):
			if (event.anchor == PANEL_ANCHOR_BOTTOM):
				# set panel width and height and add to drawing cache
				panel = event.panel
				panel.layout["top"] = self.screen_height
				panel.layout["width"] = self.screen_width
				self.panels[event.anchor] = panel

				# add space at the bottom and set menu redraw flag (_dirty_menu)
				panel_height = panel.layout["height"]
				self.screen_height = self.screen_height + panel_height
				self.resize_display()
				self._dirty_menu = True

		# when a panel is updated
		if isinstance(event, GuiPanelUpdatedEvent):
			panel = event.panel
			panel.dirty = True
			self._dirty_menu = True









