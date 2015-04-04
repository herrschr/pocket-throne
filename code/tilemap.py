class TileMap:
	TILES_SIZE = 40
	_id = -1
	tiles = []
	tiles_at = {}

	def __init__(self):
		pass

	def add_tile(self, tile_to_add):
		tiles.add(tile_to_add)
		pos_x = tile.pos_x
		pos_y = tile.pos_y
		tiles_at[pos_x, pos_y] = tile_to_add


