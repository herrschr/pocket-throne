from pygame_sdl2 import *
from core.entities.event import *
from core.managers.filemanager import FileManager

class PygameGuiManager:
	def __init__(self, eventmanager):
		# register in EventManager
		self._eventmgr = eventmanager
		self._eventmgr.register_listener(self)

		self.tilemap = None
		self.selected_tile = None

		# initialize pygame_sdl2
		global screen
		pygame_sdl2.init()
		screen = pygame_sdl2.display.set_mode((500, 500))
		screen.fill((255, 255, 255))
		pygame_sdl2.display.update()

	def draw_map(self, tilemap):
		# draw tiles
		for tile in self.tilemap.tiles:
			full_img_path = FileManager.image_path() + tile._image_path
			gui_position = self.mappos_to_gui((tile.pos_x, tile.pos_y))
			image = pygame_sdl2.image.load(full_img_path)
			screen.blit(image, gui_position)

		# draw selected tile
		if (self.selected_tile):
			selected_img_path = FileManager.image_path() + "tile_selected.png"
			selected_gui_pos = self.mappos_to_gui(self.selected_tile.get_position())
			selected_img = pygame_sdl2.image.load(selected_img_path)
			screen.blit(selected_img, selected_gui_pos)

		# draw units
		for unit in tilemap.units:
			full_img_path = FileManager.image_path() + unit.image_path
			gui_position = self.mappos_to_gui((unit.pos_x, unit.pos_y))
			image = pygame_sdl2.image.load(full_img_path)
			screen.blit(image, gui_position)

	def draw_menu(self):
		pass

	def mappos_to_gui(self,(x, y)):
		gui_x = x * self.tilemap.TILESIZE
		gui_y = y *self.tilemap.TILESIZE
		return (gui_x, gui_y)

	def gui_to_mappos(self, (x, y)):
		pos_x = int(x / self.tilemap.TILESIZE)
		pos_y = int(y / self.tilemap.TILESIZE)
		return (pos_x, pos_y)

	def on_event(self, event):
		#each tick
		if isinstance(event, TickEvent):
			if (self.tilemap):
				self.draw_map(self.tilemap)
			self.draw_menu()
			pygame_sdl2.display.flip()

		# when map is loaded
		if isinstance(event, MapLoadedEvent):
			self.tilemap = event.tilemap

		# when a tile is selected
		if isinstance(event, TileSelectedEvent):
			self.selected_tile = event.selected_tile

		# when a tile is unselected
		if isinstance(event, TileUnselectedEvent):
			self.selected_tile = None






