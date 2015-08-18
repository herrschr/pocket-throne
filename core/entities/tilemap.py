# TileMap entity holding the map
class TileMap(object):
	# engine properties
	_name = ""
	name = ""
	name_de = ""

	# map informations
	size_x = 0
	size_y = 0

	# TileMap tile collections
	tiles = []
	tiles_at = {}
	TILESIZE = 40
	_last_tile_id = -1

	# player, unit, building and item collections
	players = []
	cities = []
	units = []
	items = []

	def __init__(self):
		pass

	# set neighbors into tile entities of this map, required for generating landscape bridge images
	def initialize_neighbortiles(self):
		for tile in self.tiles:
			tile._neighbor_west =  self._get_lds_at((tile.pos_x -1, tile.pos_y))
			tile._neighbor_north =  self._get_lds_at((tile.pos_x, tile.pos_y -1))
			tile._neighbor_east = self._get_lds_at((tile.pos_x +1, tile.pos_y))
			tile._neighbor_south = self._get_lds_at((tile.pos_x, tile.pos_y +1))

	# returns the size of this map
	def get_size(self):
		return (self.size_x, self.size_y)

	# add a tile entity into this tilemap
	def add_tile(self, tile_to_add):
		# create new tile with new id
		id_to_add = self.next_tile_id()
		tile_to_add._id = id_to_add
		# get position and add Tile to tiles & tiles_at
		pos_x = tile_to_add.pos_x
		pos_y = tile_to_add.pos_y
		# add new tile to tiles and tiles_at holder lists and return it
		self.tiles.append(tile_to_add)
		self.tiles_at[pos_x, pos_y] = tile_to_add
		return tile_to_add

	# return all tiles belonging to this map
	def get_tiles(self):
		return self.tiles

	# returns tile at given position, accepts two ints
	def get_tile_at(self, pos_x, pos_y):
		return self.get_tile_at((pos_x, pos_y))

	# returns tile at given position tuple
	def get_tile_at(self, (pos_x, pos_y)):
		try:
			return  self.tiles_at[pos_x, pos_y]
		except:
			return None

	# system method
	def _get_lds_at(self, (pos_x, pos_y)):
		tile = self.get_tile_at((pos_x, pos_y))
		if tile:
			return tile.get_landscape()
		else:
			return None

	# system method
	def is_walkable_at(self, (pos_x, pos_y)):
		tile = self.get_tile_at((pos_x, pos_y))
		if tile:
			return tile.is_walkable()
		else:
			return None

	# remove tile from this map (whyever)
	def remove_tile(self, tile_to_rem):
		tiles.remove(tile_to_rem)
		tiles_at.remove(tile_to_rem)

	# returns a new, unused tile id
	def next_tile_id(self):
		self._last_tile_id += 1
		return self._last_tile_id

	# returns an xml-like representation of the TileMap
	def __repr__(self):
		return "<TileMap name=" + self.name + " size=" + str(self.get_size()) + ">"


