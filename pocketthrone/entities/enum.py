__all__ = ['Enum', 'WidgetState', 'WidgetAction']

class Enum:
	value = None

	def __init__(self, initial=None):
		self.value = initial

	def get(self):
		return self.value

	def set(self, value):
		self.value = value

	def eq(self, second):
		is_equal = False
		if self.value == second:
			is_equal = True
		return is_equal

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return "<Enum value=" + self.get() + " >"

# possible Widget states
class WidgetState(Enum):
	STATE_DEFAULT = "default"
	STATE_PRESSED = "pressed"
	STATE_DISABLED = "disabled"
	STATE_INVALID = "invalid"
	# set default
	value = STATE_DEFAULT

# possible Widget actions
class WidgetAction(Enum):
	ACTION_NONE = "default"
	ACTION_ATTACK = "attack"
	ACTION_MOVE = "move"
	ACTION_BUILD = "build"
	ACTION_NEXTTURN = "nextturn"

# possible diplomatic player relations
class PlayerRelation(Enum):
	RELATION_UNSEEN = "unseen"
	RELATION_PEACE = "peace"
	RELATION_NAP = "non-aggression-pact"
	RELATION_NEUTRAL = "neutral"
	RELATION_NEGATIVE = "negative"
	RELATION_WAR = "war"
	RELATION_GENOCIAL = "genocial"
	# set default
	value = RELATION_UNSEEN

# possible player types
class PlayerType(Enum):
	PLAYER_HUMAN = "human"
	PLAYER_AI_EASY = "ai:easy"
	PLAYER_AI_MEDIUM = "ai:medium"
	PLAYER_AI_HARD = "ai:hard"
	PLAYER_SLOT_OPEN = "slot:open"
	PLAYER_SLOT_CLOSED = "slot:closed"

# possible Tile landscapes
class TileLandscape(Enum):
	LANDSCAPE_VOID = "X"
	LANDSCAPE_WATER = "W"
	LANDSCAPE_GRASSLANDS = "G"
	LANDSCAPE_FOREST = "F"
	LANDSCAPE_DIRT = "D"
	LANDSCAPE_MOUNTAINS = "M"
	LANDSCAPE__HILLS = "H"
	LANDSCAPE_SAND = "S"
	LANDSCAPE_RIVER = "R"
	LANDSCAPE_GOLD = "*"
	LANDSCAPE_IRON = "T"
	LANDSCAPE_MARSH = "-"

# possible Tile biomes
class TileBiome(Enum):
	BIOME_UNSET = -3
	BIOME_ARCTIC = -2
	BIOME_TUNDRA = -1
	BIOME_EUROPEAN = 0
	BIOME_MEDIEVAL = 1
	BIOME_TROPICAL = 2
	BIOME_DRY = 3
	# set default
	value = BIOME_EUROPEAN

# possible City types
class CityType(Enum):
	CITY_RUINS = -1
	CITY_NONE = 0
	CITY_VILLAGE = 1
	CITY_TOWN = 2
	CITY_CAPITAL = 3
	# set default
	value = 0

# possible Building types
class BuildingType(Enum):
	BUILDING_NONE = "none"
	BUILDING_WALL = "wall"
	BUILDING_TOWER = "tower"
	BUILDING_CENTER = "towncenter"
	BUILDING_MARKETPLACE = "marketplace"
	BUILDING_STABLES = "stables"
	BUILDING_BORDEL = "bordel"
	BUILDING_BLACKSMITH = "blacksmith"
	BUILDING_HARBOR = "harbor"
	BUILDING_TUNNELS = "tunnels"
	BUILDING_SIEGEWORKSHOP = "siegeworkshop"
	BUILDING_MANSION = "mansion"
	# set default
	value = BUILDING_NONE

# possible unit type
class UnitCategory(Enum):
	UNIT_INFANTRY = "INF"
	UNIT_HEAVYINFANTRY = "HEAVY_INF"
	UNIT_CAVALERY = "CAV"
	UNIT_MACHINE = "MACHINE"
	UNIT_CIVILIAN = "CIV"

class UnitType(Enum):
	UNITTYPE_SOLIDER = "SOLDIER"
	UNITTYPE_MERCENARY = "MERC"
	UNITTYPE_GUARD = "GUARD"
	UNITTYPE_RIDDEN = "RIDDEN"
	UNITTYPE_KNIGHT = "KNIGHT"
	UNITTYPE_SPY = "SPY"
	UNITTYPE_SIEGE = "SIEGE"
	UNITTYPE_SHIP = "SHIP"

# possible weapon types
class WeaponType(Enum):
	WEAPON_SWORD = "SWORD"
	WEAPON_SPEAR = "SPEAR"
	WEAPON_BOW = "BOW"
	WEAPON_SIEGE = "SIEGE"
	WEAPON_MAGIC = "MAGIC"

