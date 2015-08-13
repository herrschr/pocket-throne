from core.entities.tile import Tile
from core.entities.tilemap import TileMap
from core.entities.unit import Unit

class UnitMovementHelper:
	DIR_WEST = 0
	DIR_NORTH = 1
	DIR_EAST = 2
	DIR_SOUTH = 3

	unit = None
	tilemap = None
	ingore_lds = False

	def __init__(self, unit, tilemap, ignore_lds=False):
		self.unit = unit
		self.tilemap = tilemap
		self.ignore_lds = ignore_lds

	# returns pseudotiles in a circle with a given radius & position
	def get_tiles_in_circle(self, (from_x, from_y), radius):
		x = radius
		y = 0
		# decision criterion divided by 2 evaluated at x=r, y=0
		decision_over_2 = 1 - x
		tiles = []

		while x >= y:
			#1
			to_add = Tile(x + from_x,  y + from_y)
			tiles.append(to_add)
			#2
			to_add = Tile(y + from_x,  x + from_y)
			tiles.append(to_add)
			#3
			to_add = Tile(-x + from_x,  y + from_y)
			tiles.append(to_add)
			#4
			to_add = Tile(-y + from_x,  x + from_y)
			tiles.append(to_add)
			#5
			to_add = Tile(-x + from_x, -y + from_y)
			tiles.append(to_add)
			#6
			to_add = Tile(-y + from_x, -x + from_y)
			tiles.append(to_add)
			#7
			to_add = Tile(x + from_x, -y + from_y)
			tiles.append(to_add)
			#8
			to_add = Tile(y + from_x, -x + from_y)
			tiles.append(to_add)

			y += 1
			# decision over 2
			if decision_over_2 <= 0:
				# change in decision criterion for y -> y+1
				decision_over_2 += 2 * y + 1
			else:
				# change for y: y+1, x -> x-1
				x -= 1
				decision_over_2 += 2 * (y - x) + 1

		return tiles

	# check if a tile is walkable by a normal unit
	def is_walkable_tile(self, pseudotile):
		tile_to_check = self.tilemap.get_tile_at(pseudotile.get_position())
		if not tile_to_check:
			return False
		if not tile_to_check.is_walkable():
			return False
		else:
			return True

	# get all possible moves in pseudotiles for the unit given in constuctor
	def get_possible_moves(self, distance=None):
		moves = []
		walkable_moves = []
		unit = self.unit

		# select all tils in filled cirlce
		if distance == None:
			distance = self.unit.mp
			curr_dist = 1
			while curr_dist <= distance:
				curr_moves = self.get_tiles_in_circle(unit.get_position(), curr_dist)
				moves.extend(curr_moves)
				curr_dist += 1

		# remove not walkable tiles
		for pseudotile in moves:
			if self.is_walkable_tile(pseudotile) and not self.ignore_lds:
				walkable_moves.append(pseudotile)
		return walkable_moves
