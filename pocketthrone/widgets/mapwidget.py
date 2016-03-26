__all__=('MapWidget')

import copy
from pprint import pprint

from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.image import Image

from pocketthrone.managers.pipe import L
from pocketthrone.entities.event import *
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.managers.filemanager import FileManager

from pocketthrone.entities.tile import Tile
from pocketthrone.entities.enum import TileLandscape, TileBiome, Compass
from pocketthrone.entities.sprite import Sprite, SpriteType

class MapWidget(Widget):
	_tag = "[MapWidget] "

	has_changed = True
	viewport_changed = True

	# actual scrolling of the map
	viewport = []
	tiles_visible = {}
	tiles_visible_incomplete = False

	prev_scrolling = {}
	scrolling = {"x": 0, "y": 0}

	def __init__(self):
		# calculate size
		super(MapWidget, self).__init__(size_hint=(1, 1))
		EventManager.register(self)
		# bind keyboard to MapWidget
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self.on_key_down)
		# initialize widget
		# load & draw map
		self._update_screen_grid()
		self._update_visible_tiles()
		# self._fill_tiles_visible()
		self.trigger_redraw()

	def _update_screen_grid(self):
		'''triggers recalculation of screen size'''
		screen_x = L.WidgetManager.get_screen_size()[0]
		screen_y = L.WidgetManager.get_screen_size()[1]
		L.WidgetManager.update_screen()

	def update(self):
		'''updates canvas when required'''
		# update list of visible tiles inside the screen
		# update map entities
		if self.has_changed:
			self.draw_map()
		# set has_changed back to False
		self.has_changed = False

	def trigger_redraw(self):
		'''triggers map redraw'''
		self.has_changed = True

	def _fill_viewport(self):
		'''initializes viewport tiles'''
		# the viewport is the representation of tile position that are actually shown on the screen
		pseudotiles = []
		# get actual scrolling relative to 0|0
		scrolling_x = abs(L.WidgetManager.get_scrolling()["x"])
		scrolling_y = abs(L.WidgetManager.get_scrolling()["y"])
		# get actual grid size fitting on monitor
		limit_x = scrolling_x + L.Grid["width"]
		limit_y = scrolling_y + L.Grid["height"]
		self.viewport = []
		# fill viewport
		for pos_x in range(scrolling_x, limit_x):
			for pos_y in range(scrolling_y, limit_y):
				pseudotile = Tile(pos_x, pos_y)
				# append pseudtile to self.viewport
				self.viewport.append(pseudotile)
		# print result
		updated_tiles = len(self.viewport)

	def shift_visible_tiles(self, plus_x=0, plus_y=0):
		pass

	def _remove_tile_row_in_viewport(self, index):
		'''removes a single grid row formerly indexed under index'''
		counter = 0
		max_tiles = L.Grid["height"] -1
		# clear from tiles_visible
		for x in range(0, max_tiles):
			self.tiles_visible[x, y] = None
			counter += 1
		self.tiles_visible
		print(self._tag + "removed " + str(counter) + " tiles from viewport cache")

	def _remove_tile_col_in_viewport(self, index):
		'''removes a single grid column formerly indexed under index'''
		counter = 0
		max_tiles = L.Grid["width"] -1
		# clear from tiles_visible
		for y in range(selfing["y"], max_tiles):
			self.tiles_visible[value, y] = None
			counter += 1
		self.tiles_visible
		print(self._tag + "removed " + str(counter) + " tiles from viewport cache")

	def _update_visible_tiles(self):
		'''update tiles in viewport'''
		# fill it with new one from TileMap when its not already loaded
		self._fill_viewport()
		counter = 0
		# for any pseudotile in self.viewport
		for pseudotile in self.viewport:
			pos_x = pseudotile.get_position()[0]
			pos_y = pseudotile.get_position()[1]
			# check if tile is already loaded in viewport tile cache
			# tile_cached = self._get_visible_tile(pos_x, pos_y)
			tile_cached = None
			if tile_cached == None:
				self._fill_visible_tile((pos_x, pos_y))
				counter += 1

	def _fill_visible_tile(self, (pos_x, pos_y)):
		'''fill a single tile in viewport tile cache at (pos_x, pos_y)'''
		# get a complete tile from MapManager
		tile_at = L.MapManager.get_tile_at((pos_x, pos_y))
		if tile_at != None:
			# add it to tiles_visible when not none
			self.tiles_visible[pos_x, pos_y] = tile_at

	# = update tiles visible on screen
	def _update_viewport(self, rel_x, rel_y):
		'''updates viewport'''
		for pseudotile in self.viewport:
			new_x = pseudotile.get_position()[0] + rel_x
			new_y = pseudotile.get_position()[1] + rel_y
			pseudotile.set_position(new_x, new_y)
		self._update_visible_tiles()

	# TODO implement
	def _add_rect(self, (grid_x, grid_y), texture_name="none"):
		scrolled_pos = L.WidgetManager.to_scrolled_pos((grid_x, grid_y))
		gui_pos = L.WidgetManager.to_gui(L.WidgetManagerto_scrolled((city.pos_x, city.pos_y)))
		texture = FileManager.get_texture(texture_name)

	def _get_viewport(self):
		'''returns list of pseutiles inside viewport'''
		return self.viewport

	def _get_visible_tile(self, pos_x, pos_y):
		'''returns a Tile from tiles_visible at position pos_x|pos_y'''
		tile_at = None
		try:
			tile_at = self.tiles_visible[pos_x, pos_y]
		finally:
			return tile_at

	def is_in_viewport(self, (pos_x, pos_y)):
		'''checks if position is inside the viewport'''
		try:
			if self.tiles_visible[pos_x, pos_y] != None:
				return self.tiles_visible[pos_x, pos_y]
			return False
		except:
			return False

	def draw_sprite(self):
		pass

	def _get_texture(self, path=None, name=None):
		if path != None:
			pass
		if name != None:
			return FileManager.get_texture(name)

	def draw_map(self):
		'''draw tilemap on widget canvas'''
		self._clean_canvas()
		self._draw_tiles()
		self._draw_cities()
		self._draw_units()

	def _clean_canvas(self):
		'''clear widget canvas'''
		self.canvas.clear()

	def _draw_tiles(self):
		''''draws tiles on widget canvas'''
		print(self._tag + "DRAW")
		# get all tiles inside the viewport when scroll position has changed
		if self.scrolling != self.prev_scrolling:
			self.position_changed = True
		# draw tiles in vp
		with self.canvas:
			for tile in self.tiles_visible.values():
				# calculate position on scrolled map
				pos = (tile.get_position()[0], tile.get_position()[1])
				scrolled_pos = L.WidgetManager.to_scrolled_pos(pos)
				gui_pos = L.WidgetManager.to_gui_pos(scrolled_pos)
				# get texture & draw Rectangle
				texture = self._get_texture(name=tile.get_texture_name())
				Rectangle(texture=texture, pos=gui_pos, size=(40, 40))

	def _draw_cities(self):
		'''draws cities on canvas'''
		# holder list for cities & buildings inside the viewport
		cities_in_viewport = []
		buildings_in_viewport = []
		# get all buildings inside the viewport
		all_buildings = []
		for city in L.CityManager.get_cities():
			all_buildings.extend(city.get_buildings())
		with self.canvas:
			# draw every city from CityManager
			print(self._tag + "draw {} cities".format(len(L.CityManager.get_cities())))
			for city in L.CityManager.get_cities():
				texture = self._get_texture(name=city.get_image_path())
				flag_texture = self._get_texture(name=city.flag_source())
				pos_x = city.get_position()[0]
				pos_y = city.get_position()[1]
				scrolled_pos = L.WidgetManager.to_scrolled_pos((pos_x, pos_y))
				gui_pos = L.WidgetManager.to_gui_pos(scrolled_pos)
				Rectangle(texture=flag_texture, pos=gui_pos, size=(40, 80))
				Rectangle(texture=texture, pos=gui_pos, size=(40, 80))
			# draw buildings
			for building in all_buildings:
				texture = self._get_texture(name=building.get_image_path())
				pos_x = building.get_position()[0]
				pos_y = building.get_position()[1]
				scrolled_pos = L.WidgetManager.to_scrolled_pos((pos_x, pos_y))
				gui_pos = L.WidgetManager.to_gui_pos(scrolled_pos)
				Rectangle(texture=texture, pos=gui_pos, size=(40, 40))
			# at least draw selected tile
			if L.MapManager.has_selected_tile == True:
				texture = self._get_texture(name="tile_selected")
				pos_x = L.MapManager.get_selected_tile().get_position()[0]
				pos_y = L.MapManager.get_selected_tile().get_position()[1]
				scrolled_pos = L.WidgetManager.to_scrolled_pos((pos_x, pos_y))
				gui_pos = L.WidgetManager.to_gui_pos(scrolled_pos)
				Rectangle(texture=texture, pos=gui_pos, size=(40, 40))

	def _draw_units(self):
		'''draws units on canvas'''
		units_in_viewport = []
		# get all units inside the viewport
		for unit in L.UnitManager.get_units():
			unit_pos = unit.get_position()
			if self.is_in_viewport(unit_pos):
				units_in_viewport.append(unit)
		with self.canvas:
			# draw any unit inside the viewport
			for unit in units_in_viewport:
				texture = self._get_texture(name=unit.image_path)
				pos_x = unit.get_position()[0]
				pos_y = unit.get_position()[1]
				scrolled_pos = L.WidgetManager.to_scrolled_pos((pos_x, pos_y))
				gui_pos = L.WidgetManager.to_gui_pos(scrolled_pos)
				Rectangle(texture=texture, pos=gui_pos, size=(40, 40))

			# draw possible unit moves and attacks
			if L.UnitManager.has_selected_unit():
				for pseudotile in L.UnitManager.selected_unit_moves:
					texture = self._get_texture(name="tile_oo_possiblemove")
					gui_pos = L.WidgetManager.to_gui_pos(L.WidgetManager.to_scrolled_pos((pseudotile.pos_x, pseudotile.pos_y)))
					Rectangle(texture=texture, pos=gui_pos, size=(40, 40))
				for pseudotile in L.UnitManager.selected_unit_attacks:
					texture = self._get_texture(name="tile_oo_possibleattack")
					gui_pos = L.WidgetManager.to_gui_pos(L.WidgetManager.to_scrolled_pos((pseudotile.pos_x, pseudotile.pos_y)))
					Rectangle(texture=texture, pos=gui_pos, size=(40, 40))

	def on_key_down(self, keyboard, keycode, text, mods):
		'''triggered when keyboard was pressed'''
		key_pressed = keycode[1]
		ey_key_down = KeyPressedEvent(key_pressed)
		EventManager.fire(ey_key_down)

	def _keyboard_closed(self):
		'''closes keyboard connection'''
		self._keyboard.unbind(on_key_down=self.on_key_down)
		self._keyboard = None

	def on_touch_down(self, touch):
		'''triggered when the mouse is pressed'''
		touch_inv_y = Window.height - touch.y
		# on left click
		if touch.button == "left":
			# fire MouseClickedEvent
			ev_mouse_clicked = MouseClickedEvent((touch.x, touch_inv_y))
			EventManager.fire(ev_mouse_clicked)
			# get the grid position that's clicked
			grid_pos = L.WidgetManager.to_grid_pos((touch.x, touch_inv_y))
			# calculate the real position in by adding the map scrolling
			scrolled_x = grid_pos[0] - self.scrolling["x"]
			scrolled_y = grid_pos[1] - self.scrolling["y"]
			# select correct tile in MapManager
			L.MapManager.select_tile_at((scrolled_x, scrolled_y))
		# on right click
		elif touch.button == "right":
			ev_mouse_rightclicked = MouseRightClickedEvent((touch.x, touch_inv_y))
			EventManager.fire(ev_mouse_rightclicked)

	def on_touch_up(self, touch):
		'''triggered wehn the mouse was released'''
		# get touch position & position in grid
		touch_inv_y = Window.height - touch.y
		touch_pos = (touch.x, touch_inv_y)
		grid_pos = L.WidgetManager.to_grid_pos(touch_pos)

		# add map scrolling parameters
		# self_x(grid_pos[0])
		# self_y(grid_pos[1])

		# fire MouseReleasedEvent
		if touch.button == "left":
			ev_mouse_released = MouseReleasedEvent(touch_pos, grid_pos)
			EventManager.fire(ev_mouse_released)
			# update scrolling

	def scroll(self, (plus_x, plus_y)):
		'''scrolls map by relative position'''
		# backup recent scrolling state
		scr_prev = copy.deepcopy(self.scrolling)
		# make new scrolling state
		new_x = int(scr_prev["x"]) + int(plus_x)
		new_y = int(scr_prev["y"]) + int(plus_y)
		scr_new = {"x": int(new_x), "y": int(new_y)}
		self.scrolling = scr_new
		# fire MapScrolledEvent
		ev_map_scrolled = MapScrolledEvent(scr_new, scr_prev)
		EventManager.fire(ev_map_scrolled)
		# update viewport
		self._update_visible_tiles()
		self.trigger_redraw()

	def scroll_at(self, (grid_x, grid_y)):
		'''center map on position'''
		# get half of the grids dimension
		half_x = int(L.WidgetManager.get_grid()["width"] /2)
		half_y = int(L.WidgetManager.get_grid()["height"] /2)
		# scroll to 0|0
		null_x = -1 * L.MapManager.get_scrolling()["x"]
		null_y = -1 * L.MapManager.get_scrolling()["y"]
		self.scroll((null_x, null_y))
		# get scrolling centered on given position
		mid_x = half_x - grid_x
		mid_y = half_y - grid_y
		# update actual scrolling
		self.scroll((mid_x, mid_y))

	def scroll_x(self, plus_x):
		'''scroll horizontally'''
		self.scroll((plus_x, 0))

	def scroll_y(self, plus_y):
		'''scroll vertically'''
		self.scroll((0, plus_y))

	def on_event(self, event):
		# redraw the map when required each TickEvent
		if isinstance(event, TickEvent):
			self.update()

		# update map cache
		if isinstance(event, GameStartedEvent):
			print(self._tag + "MAP LOADED")
			self._update_screen_grid()
			self._update_visible_tiles()
			self.trigger_redraw()

		# handle tiles_visible press for scrolling the widget
		if isinstance(event, KeyPressedEvent):
			if event.key == "up":
				self.scroll_y(-1)
			elif event.key == "down":
				self.scroll_y(1)
			elif event.key == "left":
				self.scroll_x(-1)
			elif event.key == "right":
				self.scroll_x(1)

		# redraw the map when an entity is (un-)selected
		if isinstance(event, TileSelectedEvent):
			self.trigger_redraw()
		if isinstance(event, UnitSelectedEvent):
			self.trigger_redraw()
		if isinstance(event, UnitMovedEvent):
			self.trigger_redraw()
		if isinstance(event, UnitSpawnedEvent):
			self.trigger_redraw()

		# map was scrolled after user input
		if isinstance(event, MapScrolledEvent):
			# cache previous scrolling offset
			prev_scrolling = {"x": int(event.prev_x), "y": int(event.prev_y)}
			self.prev_scrolling = prev_scrolling
			# update actual scrolling offset
			new_scrolling = {"x": int(event.new_x), "y": int(event.new_y)}
			self.scrolling = new_scrolling
