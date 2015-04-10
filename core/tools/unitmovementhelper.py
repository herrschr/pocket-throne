from core.entities.tile import Tile
from core.entities.tilemap import TileMap
from core.entities.unit import Unit

class UnitMovementHelper:
	DIR_WEST = 0
	DIR_NORTH = 1
	DIR_EAST = 2
	DIR_SOUTH = 3

	def __init__(self, unit, tilemap):
		self.unit = unit
		self.tilemap = tilemap

	def check_direction(self, (from_x, from_y), dir, mp):
		print("check dir: " + str(dir))
		possible_moves = []
		while mp > 0:
			# check towards west: x--
			if dir == self.DIR_WEST and from_x >= 0:
				from_x -= 1
			# check towards north: y--
			if dir == self.DIR_NORTH and from_y >= 0:
				from_y -= 1
			# check towards east: x++
			if dir == self.DIR_EAST and from_x < self.tilemap.size_x:
				from_x += 1
			# check towards south: y++
			if dir == self.DIR_SOUTH and from_y < self.tilemap.size_y:
				from_y += 1
			# check if tile is solid
			tile_to_check = self.tilemap.get_tile_at((from_x, from_y))
			if not tile_to_check:
				return possible_moves
			if not tile_to_check.is_walkable():
				print ("Unit Movement impossible to x=" + str(from_x) + " y=" + str(from_y))
				return possible_moves
			pseudotile = Tile(from_x, from_y)
			possible_moves.append(pseudotile)
			print ("Unit Movement possible to x=" + str(from_x) + " y=" + str(from_y))
			mp -= 1
		return possible_moves

	def get_possible_moves(self):
		moves = []
		unit = self.unit
		towards_dir = 0
		while towards_dir < 4:
			pseudotiles = self.check_direction(unit.get_position(), towards_dir, unit.mp)
			moves += pseudotiles
			print("moves: " + str(len(moves)))
			towards_dir += 1
		return moves
