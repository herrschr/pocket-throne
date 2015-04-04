class TileMap:
	_id = -1
	name = ""
	TILES_SIZE = 40
	tiles = []
	tiles_at = {}

	def __init__(self):
		pass

	def add_tile(self, tile_to_add):
		tiles.add(tile_to_add)
		pos_x = tile.pos_x
		pos_y = tile.pos_y
		tiles_at[pos_x, pos_y] = tile_to_add

	def get_tile_at(pos_x, pos_y):
		return  tiles_at[pos_x, pos_y]

	def remove_tile(self, tile_to_rem):
		tiles.remove(tile_to_rem)
		tiles_at.remove(tile_to_rem)

