from kivy.graphics import Color, Ellipse, Rectangle, Fbo
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.image import Image

from core.managers.locator import Locator
from core.entities.event import *
from core.managers.eventmanager import EventManager
from core.managers.filemanager import FileManager

class MapWidget(Widget):
	_dirty = True
	_map = None

	scrolled_x = 0
	scrolled_y = 0
	grid_width = 0
	grid_height = 0

	def __init__(self, **kwargs):
		super(MapWidget, self).__init__(**kwargs)
		# register in eventmanager
		EventManager.register_listener(self)
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down = self.on_key_down)
		# initialize widget
		self.grid_width = int(Window.width / 40) +1
		self.grid_height = int(Window.height / 40) +1
		# load & draw map
		self._map = Locator.TILEMAP
		self.trigger_redraw()

	# update the canvas when a redraw is required
	def update(self):
		if self._dirty:
			self.draw_map()

	# trigger a canvas redraw
	def trigger_redraw(self):
		self._dirty = True

	# translate a pixel position into the tile grid
	def to_map(self, (pos_x, pos_y)):
		map_x = int(pos_x / Locator.TILEMAP.TILESIZE)
		map_y = int(pos_y / Locator.TILEMAP.TILESIZE)
		inv_y = Locator.TILEMAP.size_y - map_y
		return map_x, map_y

	# translate a tile grid position into a pixel pos
	def to_gui(self, (map_x, map_y), y_inv=True):
		gui_x = self.x + (map_x *40)
		gui_y = self.y + ((map_y +1) *40)
		inv_y = self.top - gui_y
		if y_inv:
			return (gui_x, inv_y)
		else:
			return (gui_x, gui_y)

	def to_scrolled(self, (map_x, map_y)):
		scrolled_x = map_x - self.scrolled_x
		scrolled_y = map_y - self.scrolled_y
		return (scrolled_x, scrolled_y)

	def is_in_viewport(self, (grid_x, grid_y)):
		print("viewport="+ str((self.scrolled_x, self.scrolled_y, self.scrolled_x + self.grid_width, self.scrolled_y + self.grid_height)))
		if grid_x >= self.scrolled_x and grid_x <= self.scrolled_x + self.grid_width:
			if grid_y >= self.scrolled_y and grid_y <= self.scrolled_y + self.grid_height:
				return True
		return False

	# draw the map on the widget canvas
	def draw_map(self):
		# add tiles to draw
		tiles_in_viewport = []
		units_in_viewport = []
		cities_in_viewport = []
		# get all tiles inside the viewport
		for iy in range(self.scrolled_y, self.scrolled_y + self.grid_height):
			for ix in range(self.scrolled_x, self.scrolled_x + self.grid_width):
				tile = Locator.TILEMAP.get_tile_at((ix, iy))
				if tile != None:
					tiles_in_viewport.append(tile)
		# get all units inside the viewport
		for unit in Locator.UNIT_MGR.get_units():
			pass

		# clear the canvas
		with self.canvas:
			self.canvas.clear()
			for tile in tiles_in_viewport:
				gui_pos = self.to_gui(self.to_scrolled((tile.pos_x, tile.pos_y)))
				# load the tile texture
				source = FileManager.image_path() + tile.get_image_path()
				# draw an rectangle with the tile texture
				Rectangle(source=source, pos=gui_pos, size=(40, 40))
			# draw selected tile
			if Locator.MAP_MGR.selected_tile != None:
				selected_tile = Locator.MAP_MGR.selected_tile
				texture = Image(FileManager.image_path() + "tile_selected.png").texture
				gui_pos = self.to_gui(self.to_scrolled((selected_tile.pos_x, selected_tile.pos_y)))
				Rectangle(texture=texture, pos=gui_pos, size=(40, 40))
			# draw cities
			for city in Locator.CITY_MGR._cities:
				texture = Image(FileManager.image_path() + "city_village.png").texture
				gui_pos = self.to_gui(self.to_scrolled((city.pos_x, city.pos_y)))
				Rectangle(texture=texture, pos=gui_pos, size=(40, 80))
			# draw units
			for unit in Locator.UNIT_MGR._units:
				texture = Image(FileManager.image_path() + unit.image_path).texture
				gui_pos = self.to_gui(self.to_scrolled((unit.pos_x, unit.pos_y)))
				Rectangle(texture=texture, pos=gui_pos, size=(40, 40))
			# draw possible unit moves and attacks
			if Locator.UNIT_MGR._selected:
				for pseudotile in Locator.UNIT_MGR._selected_moves:
					texture = Image(FileManager.image_path() + "overlay_unit_possiblemove.png").texture
					gui_pos = self.to_gui(self.to_scrolled((pseudotile.pos_x, pseudotile.pos_y)))
					Rectangle(texture=texture, pos=gui_pos, size=(40, 40))
				for pseudotile in Locator.UNIT_MGR._selected_attacks:
					texture = Image(FileManager.image_path() + "overlay_unit_possibleattack.png").texture
					gui_pos = self.to_gui(self.to_scrolled((pseudotile.pos_x, pseudotile.pos_y)))
					Rectangle(texture=texture, pos=gui_pos, size=(40, 40))
		self._dirty = False

	def on_touch_down(self, touch):
		# fire MouseClickedEvent
		touch_inv_y = Window.height - touch.y
		ev_mouse_clicked = MouseClickedEvent((touch.x, touch_inv_y))
		EventManager.fire(ev_mouse_clicked)
		# set the selcted tile in MapManager
		grid_pos = self.to_map((touch.x, touch_inv_y))
		scrolled_x = self.scrolled_x + grid_pos[0]
		scrolled_y = self.scrolled_y + grid_pos[1]
		Locator.MAP_MGR.select_tile_at((scrolled_x, scrolled_y))

	def scroll_x(self, tiles):
		self.scrolled_x += tiles
		self.trigger_redraw()

	def scroll_y(self, tiles):
		self.scrolled_y += tiles
		self.trigger_redraw()

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down = self.on_key_down)
		self._keyboard = None

	def on_key_down(self, keyboard, keycode, text, modifiers):
		ev_key_pressed = KeyPressedEvent(keycode[1])
		EventManager.fire(ev_key_pressed)

	def on_touch_move(self, touch):
		print("Map moved " + str(self.parent.to_window(self.parent.x, self.parent.y)))

	def on_event(self, event):
		# update the map when required
		if isinstance(event, TickEvent):
			self.update()
		# handle key press for scrolling the widget
		if isinstance(event, KeyPressedEvent):
			if event.key == "up":
				self.scroll_y(-1)
			elif event.key == "down":
				self.scroll_y(1)
			elif event.key == "left":
				self.scroll_x(-1)
			elif event.key == "right":
				self.scroll_x(1)
		# redraw the map on various events
		if isinstance(event, TileSelectedEvent):
			self.trigger_redraw()
		if isinstance(event, UnitSelectedEvent):
			self.trigger_redraw()
		if isinstance(event, UnitMovedEvent):
			self.trigger_redraw()
		if isinstance(event, UnitSpawnedEvent):
			self.trigger_redraw()
