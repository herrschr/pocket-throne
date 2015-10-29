from copy import deepcopy
# Weapon class for std-unit or hero, defines the dealed damage, defined in <unit>.weapon
class Weapon(object):
	# engine properties
	name = ""
	name_de = ""

	# weapon category (SWORD, SPEAR, BOW)
	category = None
	# weapon constants
	value = 1
	distance = 1

	# chance to hit the enemy unit
	hit_chance = 50

	# default damage multiplier
	multiplier_vs_category = {}

	def __init__(self, category):
		self.category = category

	# returns the default multiplier vs. an unit category
	def get_default_multiplier(self, weapon_type):
		multiplier = None
		if weapon_type == "SWORD":
			multiplier = {
				"INF": 1,
				"HEAVY_INF": 0.5,
				"CAV": 0.4,
				"MACHINE": 0.8}
		elif weapon_type == "SPEAR":
			multiplier = {
				"INF": 0.4,
				"HEAVY_INF": 0.6,
				"CAV": 1,
				"MACHINE": 1}
		elif weapon_type == "BOW":
			multiplier = {
				"INF": 1,
				"HEAVY_INF": 0.4,
				"CAV": 0.6,
				"MACHINE": 0.2}
		return multiplier

	# merge default damage multipliers with weapon specific ones
	def merge_attack_multipliers(self):
		default_multiplier = self.get_default_multiplier(self.category)
		wpn_multiplier = deepcopy(self.multiplier_vs_category)
		unit_categories = ["INF", "HEAVY_INF", "CAV", "MACHINE"]
		# set default dmg multiplier when no specific one is set
		for i in range(0,3):
			unit_category = unit_categories[i]
			default_damage = default_multiplier[unit_category]
			wpn_damage = wpn_multiplier.get(unit_category, None)
			if not wpn_damage:
				self.multiplier_vs_category[unit_category] = default_damage

	# returns the calculated weapon damage vs. an unit category
	def get_damage_vs(self, unit_category):
		multiplier = self.multiplier_vs_category[unit_category]
		damage = multiplier * self.damage
		return damage
