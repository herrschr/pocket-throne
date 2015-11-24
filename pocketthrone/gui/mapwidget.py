__all__=('MapWidget')

import copy

from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.image import Image

from pocketthrone.managers.locator import Locator
from pocketthrone.entities.event import *
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.managers.filemanager import FileManager

from pocketthrone.entities.tile import Tile

class MapWidget(Widget):
	_tag = "[MapWidget] "
	_dirty = True
	has_changed = True

	# actual scrolling of the map
	tiles_in_viewport = []
	last_scrolling = {}
	scrolling = {
		"x": 0,
		"y": 0
	}

	# number of tiles that are fitting in the map size
	grid_width = 0
	grid_height = 0

	def __init__(self):
		widget_size = (Locator.TILEMAP.size_x *40, Locator.TILEMAP.size_y *40, )
		super(MapWidget, self).__init__(size_hint=(1, 1))
		EventManager.register_listener(self)
		# register in eventmanager
		Locator.GUI_MGR.register_widget("mapwidget", self)
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down = self.on_key_down)
		# initialize widget
		self.grid_width = Locator.TILEMAP.size_x
		self.grid_width = Locator.TILEMAP.size_y
		# load & draw map

	def update_screen_grid(self):
		screen_x = Locator.GUI_MGR.get_screen_size()[0]
		screen_y = Locator.GUI_MGR.get_screen_size()[1]
		self.grid_width = int(screen_x / 40) +1
		self.grid_height = int(screen_y / 40) +1

	# update the canvas when a redraw is required
	def update(self):
		if self._dirty:
			print(self._tag + "dirty")
			self.update_screen_grid()
			self.draw_map()

	# trigger a redraw of the map
	def trigger_redraw(self):
		self._dirty = True

	# translate a screen position into the tile grid
	def to_map(self, (pos_x, pos_y)):
		map_x = int(pos_x / Locator.TILEMAP.TILESIZE)
		map_y = int(pos_y / Locator.TILEMAP.TILESIZE)
		inv_y = Locator.TILEMAP.size_y - map_y
		return map_x, map_y

	# translate a tile grid position into a position on the screen
	def to_gui(self, (map_x, map_y), y_inv=True):
		gui_x = self.x + (map_x *40)
		gui_y = self.y + ((map_y +1) *40)
		inv_y = self.top - gui_y
		if y_inv:
			return (gui_x, inv_y)
		else:
			return (gui_x, gui_y)

	# translate a grid position into a grid position considering the actual map scrolling
	def to_scrolled(self, (map_x, map_y)):
		scrolled_x = map_x - self.scrolling["x"]
		scrolled_y = map_y - self.scrolling["y"]
		return (scrolled_x, scrolled_y)

	# checks if a grid position is inside the screen considering the actual map scrolling
	def is_in_viewport(self, (pos_x, pos_y)):
		# calculate viewport bottom & right
		limit_x = self.scrolling["x"] + self.grid_width
		limit_y = self.scrolling["y"] + self.grid_height
		# check if poition is inside the viewports bounds
		if pos_y < self.scrolling["y"] and pos_x > limit_y:
			if pos_x < self.scrolling["x"] and pos_x > limit_x:
				return True
		return False

	# draw the map on the widget canvas
	def draw_map(self):
		if self._dirty:
			# clear anything
			self.canvas.clear()
			# draw all tiles visible with the actual map scrolling
			self._draw_tiles()
			# draw cities
			self._draw_cities()
			# draw units
			self._draw_units()

	# draw any tiles that are inside the map viewport
	def _draw_tiles(self):
		position_changed = False
		# get all tiles inside the viewport when scroll position has changed
		if self.scrolling != self.last_scrolling:
			self.position_changed = True
		#when position is unchanged
		if not self.position_changed:
			print(self._tag + " scrolling unchanged")
		# when map was scrolled
		else:
			print(self._tag + "scrolling CHANGED")
			pseudotiles_in_vp = self.get_viewport_tiles()
			tiles_in_vp = []
			# load tiles in viewport
			for pseudotile in pseudotiles_in_vp:
				tile = Locator.TILEMAP.get_tile_at(pseudotile.get_position())
				tiles_in_vp.append(tile)
			print (self._tag + "loaded " + str(len(tiles_in_vp)) + " tiles in viewport cache")
			self.tiles_in_viewport = tiles_in_vp

			# draw tiles in vp
			for tile in self.tiles_in_viewport:
				gui_pos = self.to_gui(self.to_scrolled((tile.get_position())))
				texture = Image(FileManager.image_path() + tile.get_image_path()).texture
				Rectangle(texture=texture, pos=gui_pos, size=(40, 40))

	def get_viewport_tiles(self):
		pseudotiles = []
		vp_x = self.scrolling["x"]
		vp_y = self.scrolling["y"]
		vp_w = self.grid_width
		vp_h = self.grid_height

		for ver in range(vp_y, vp_y + vp_h):
			for hor in range(vp_x, vp_x+ vp_w):
				tile = Tile(hor, ver)
				pseudotiles.append(tile)
		return pseudotiles

	# draw any city and building inside the viewport
	def _draw_cities(self):
		# holder list for cities & buildings inside the viewport
		cities_in_viewport = []
		buildings_in_viewport = []
		# get all buildings inside the viewport
		buildings = []
		for city in Locator.CITY_MGR.get_cities():
			buildings.extend(city.get_buildings())
		for building in buildings:
			bld_pos = building.get_position()
			if self.is_in_viewport(bld_pos):
				buildings_in_viewport.append(building)

		# draw every city from CityManager
		for city in Locator.CITY_MGR.get_cities():
			texture = Image(FileManager.image_path() + city.get_image_path()).texture
			gui_pos = self.to_gui(self.to_scrolled((city.pos_x, city.pos_y)))
			Rectangle(texture=texture, pos=gui_pos, size=(40, 80))
		# draw buildings
		for building in buildings_in_viewport:
			texture = Image(FileManager.image_path() + building.get_image_path()).texture
			gui_pos = self.to_gui(self.to_scrolled((building.get_position())))
			Rectangle(texture=texture, pos=gui_pos, size=(40, 40))

	# draw any unit inside the viewport
	def _draw_units(self):
		units_in_viewport = []
		# get all units inside the viewport
		for unit in Locator.UNIT_MGR.get_units():
			unit_pos = unit.get_position()
			if self.is_in_viewport(unit_pos):
				units_in_viewport.append(unit)
		# draw any unit inside the viewport
		for unit in units_in_viewport:
			texture = Image(FileManager.image_path() + unit.image_path).texture
			gui_pos = self.to_gui(self.to_scrolled((unit.pos_x, unit.pos_y)))
			Rectangle(texture=texture, pos=gui_pos, size=(40, 40))
		# draw possible unit moves and attacks
		if Locator.UNIT_MGR.has_selected_unit():
			for pseudotile in Locator.UNIT_MGR.selected_unit_moves:
				texture = Image(FileManager.image_path() + "overlay_unit_possiblemove.png").texture
				gui_pos = self.to_gui(self.to_scrolled((pseudotile.pos_x, pseudotile.pos_y)))
				Rectangle(texture=texture, pos=gui_pos, size=(40, 40))
			for pseudotile in Locator.UNIT_MGR.selected_unit_attacks:
				texture = Image(FileManager.image_path() + "overlay_unit_possibleattack.png").texture
				gui_pos = self.to_gui(self.to_scrolled((pseudotile.pos_x, pseudotile.pos_y)))
				Rectangle(texture=texture, pos=gui_pos, size=(40, 40))

	def backup_scolling_position(self):
		self.last_scrolling["x"] = copy.deepcopy(self.scrolling["x"])
		self.last_scrolling["y"] = copy.deepcopy(self.scrolling["y"])

	# select correct tile on mouse click
	def on_touch_down(self, touch):
		# translate y pos (0|0 is on top left of the window)
		touch_inv_y = Window.height - touch.y
		# on left click
		if touch.button == "left":
			# fire MouseClickedEvent
			ev_mouse_clicked = MouseClickedEvent((touch.x, touch_inv_y))
			EventManager.fire(ev_mouse_clicked)
			# get the grid position that's clicked
			grid_pos = self.to_map((touch.x, touch_inv_y))
			# calculate the real position in by adding the map scrolling
			self.scroll_x(grid_pos[0])
			scrolled_x = self.scrolling["x"] + grid_pos[0]
			scrolled_y = self.scrolling["y"] + grid_pos[1]
			# select correct tile in MapManager
			Locator.MAP_MGR.select_tile_at((scrolled_x, scrolled_y))
		# on right click
		elif touch.button == "right":
			ev_mouse_rightclicked = MouseRightClickedEvent((touch.x, touch_inv_y))
			EventManager.fire(ev_mouse_rightclicked)

	# fire MouseReleasedEvent on mouse drag movement
	def on_touch_up(self, touch):
		# get touch position & position in grid
		touch_inv_y = Window.height - touch.y
		touch_pos = (touch.x, touch_inv_y)
		grid_pos = self.to_map(touch_pos)

		# add map scrolling parameters
		self.scroll_x(grid_pos[0])
		self.scroll_y(grid_pos[1])

		# fire MouseReleasedEvent
		if touch.button == "left":
			ev_mouse_released = MouseReleasedEvent(touch_pos, grid_pos)
			EventManager.fire(ev_mouse_released)

	# scroll horizontally
	def scroll_x(self, value):
		self.backup_scolling_position()
		self.scrolling["x"] += value
		self.trigger_redraw()

	# scroll vertically
	def scroll_y(self, value):
		self.backup_scolling_position()
		self.scrolling["y"] += value
		self.trigger_redraw()

	# on keyboad close
	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down = self.on_key_down)
		self._keyboard = None

	# fire KeyPressedEvent on key press
	def on_key_down(self, keyboard, keycode, text, modifiers):
		ev_key_pressed = KeyPressedEvent(keycode[1])
		EventManager.fire(ev_key_pressed)

	def on_event(self, event):
		# redraw the map when required each TickEvent
		if isinstance(event, TickEvent):
			self.update()
			self._dirty = False
		# update map cache
		if isinstance(event, MapLoadedEvent):
			print(self._tag + "MAP LOADED")
			self._map = event.tilemap
			self.trigger_redraw()
		# handle key press for scrolling the widget
		if isinstance(event, KeyPressedEvent):
			if event.key == "up":
				self.scroll_y(-2)
			elif event.key == "down":
				self.scroll_y(2)
			elif event.key == "left":
				self.scroll_x(-2)
			elif event.key == "right":
				self.scroll_x(2)
		# redraw the map on various events
		if isinstance(event, TileSelectedEvent):
			self.trigger_redraw()
		if isinstance(event, UnitSelectedEvent):
			self.trigger_redraw()
		if isinstance(event, UnitMovedEvent):
			self.trigger_redraw()
		if isinstance(event, UnitSpawnedEvent):
			self.trigger_redraw()
