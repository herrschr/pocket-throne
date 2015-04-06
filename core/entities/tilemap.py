class TileMap(object):
	# TileMap system properties
	_name = ""
	_last_tile_id = -1
	TILESIZE = 40

	# TileMap class properties
	name = ""
	name_de = ""
	size_x = 0
	size_y = 0

	# TileMap tile collections
	tiles = []
	tiles_at = {}

	# unit, building and item collections
	units = []
	buildings = []
	items = []

	def __init__(self):
		pass

	def get_size(self):
		return (self.size_x, self.size_y)

	# add a Tile (core/entities/tile.py)
	def add_tile(self, tile_to_add):
		# generate new id
		id_to_add = self.next_tile_id()
		tile_to_add._id = id_to_add
		# get position and add Tile to tiles & tiles_at
		pos_x = tile_to_add.pos_x
		pos_y = tile_to_add.pos_y
		self.tiles.append(tile_to_add)
		self.tiles_at[pos_x, pos_y] = tile_to_add
		return tile_to_add

	# returns tile at given position, accepts two ints
	def get_tile_at(self, pos_x, pos_y):
		return  self.get_tile_at((pos_x, pos_y))

	# returns tile at given position tuple
	def get_tile_at(self, (pos_x, pos_y)):
		try:
			return  self.tiles_at[pos_x, pos_y]
		except:
			return None

	# remove tile
	def remove_tile(self, tile_to_rem):
		tiles.remove(tile_to_rem)
		tiles_at.remove(tile_to_rem)

	# returns a new, unused tile id
	def next_tile_id(self):
		self._last_tile_id += 1
		return self._last_tile_id

	def __repr__(self):
		return "<TileMap name=" + self.name + " size=" + str(self.get_size()) + ">"


