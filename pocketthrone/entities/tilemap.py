from pocketthrone.entities.enum import Enum, CoordinateAxis, Compass

class GridTranslation:
	axis = None
	value = 0

	def __init__(self, axis=CoordinateAxis.AXIS_X, value=0):
		self.axis = axis
		self.value = value

	# return the relative position of the vector represented by this class
	def get_relative_position(self):
		if self.axis == CoordinateAxis.AXIS_X:
			return(self.value, 0)
		else:
			return(0, self.value)

# TileMap entity holding the map
class TileMap(object):
	# engine properties
	_name = ""
	_tag = "[TileMap] "
	name = ""
	name_de = ""
	initialized = False

	# map informations
	size_x = 0
	size_y = 0

	# TileMap tile collections
	tiles = []
	tiles_at = {}
	TILESIZE = 40
	_last_tile_id = -1

	# player, unit, building and masterwork collections
	players = []
	cities = []
	units = []
	masterworks = []

	def __init__(self):
		pass

	# set neighbors into tile entities of this map, required for generating landscape bridge images
	def _initialize_neighbors(self):
		updated = []
		updated_at = {}
		counter = 0
		dirs = [Compass.DIRECTION_WEST, Compass.DIRECTION_NORTH, Compass.DIRECTION_EAST, Compass.DIRECTION_SOUTH]
		for tile in self.tiles:
			tile_x = tile.get_position()[0]
			tile_y = tile.get_position()[1]
			for direction in dirs:
				neighbor_x = tile_x + direction[0]
				neighbor_y = tile_y + direction[1]
				neighbor_tile = self._get_tile_at((neighbor_x, neighbor_y))
				if neighbor_tile:
					tile.neighbors[direction] = neighbor_tile.landscape
			updated.append(tile)
			updated_at[tile_x, tile_y] = tile
			counter += 1
		print(self._tag + "neighbors for " + str(counter) + " tiles set.")
		self.tiles = updated
		self.initialized = True

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

	def get_masterworks(self):
		return self.masterworks

	def get_players(self):
		return self.players

	# returns tile at given position, accepts two ints
	def get_tile_at(self, pos_x, pos_y):
		return self.get_tile_at((pos_x, pos_y))

	# returns tile at given position tuple
	def get_tile_at(self, (pos_x, pos_y)):
		if not self.initialized:
			self._initialize_neighbors
		return self._get_tile_at((pos_x, pos_y))

	def _get_tile_at(self, (pos_x, pos_y)):
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
