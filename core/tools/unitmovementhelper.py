from core.entities.tile import Tile
from core.entities.tilemap import TileMap
from core.entities.unit import Unit

class UnitMovementHelper:
	DIR_WEST = 0
	DIR_NORTH = 1
	DIR_EAST = 2
	DIR_SOUTH = 3

	def __init__(self, unit, map):
		self.unit = unit
		self.map = map
		self.moves = []

	def check_direction(self, (from_x, from_y), dir, mp):
		print("check dir: " + str(dir))
		possible_moves = []
		while mp > 0:
			# check towards west: x--
			if dir == self.DIR_WEST:
				from_x -= 1
			# check towards north: y--
			if dir == self.DIR_NORTH:
				from_y -= 1
			# check towards east: x++
			if dir == self.DIR_EAST:
				from_x += 1
			# check towards south: y++
			if dir == self.DIR_SOUTH:
				from_y += 1
			# check if tile is solid
			tile_to_check = self.map.get_tile_at((from_x, from_y))
			if not tile_to_check:
				return
			if not tile_to_check.is_walkable():
				return
			pseudotile = Tile(from_x, from_y)
			possible_moves.append(pseudotile)
			print ("Unit Movement possible to x=" + str(from_x) + " y=" + str(from_y))
			mp -= 1
		return possible_moves

	def get_possible_moves(self):
		unit = self.unit
		towards_dir = 0
		while towards_dir < 4:
			pseudotiles = self.check_direction(unit.get_position(), towards_dir, unit.mp)
			self.moves += pseudotiles
			towards_dir += 1
		return self.moves
