class TileMap(object):
	# static TileMap vars
	_id = -1
	name = ""
	TILES_SIZE = 40

	# TileMap tile collections
	tiles = []
	tiles_at = {}
	_last_tile_id = -1

	def __init__(self):
		pass

	# add a Tile (code/tile.py)
	def add_tile(self, tile_to_add):
		id_to_add = self.next_tile_id()
		self.tiles.append(tile_to_add)
		pos_x = tile_to_add.pos_x
		pos_y = tile_to_add.pos_y
		self.tiles_at[pos_x, pos_y] = tile_to_add
		return tile_to_add

	# returns tile at given position
	def get_tile_at(pos_x, pos_y):
		return  tiles_at[pos_x, pos_y]

	# remove tile
	def remove_tile(self, tile_to_rem):
		tiles.remove(tile_to_rem)
		tiles_at.remove(tile_to_rem)

	# returns a new, unused tile id
	def next_tile_id(self):
		self._last_tile_id += 1
		return self._last_tile_id


