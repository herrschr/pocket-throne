from copy import deepcopy
from pocketthrone.entities.enum import WeaponType, UnitType, UnitCategory
# Weapon class for std-unit or hero, defines the dealed damage, defined in <unit>.weapon
class Weapon(object):
	# engine properties
	name = ""
	name_de = ""

	# weapon category (SWORD, SPEAR, BOW)
	weapon_type = WeaponType(initial=WeaponType.WEAPON_SWORD)
	# weapon constants
	value = 1
	distance = 1

	# chance to hit the enemy unit
	hit_chance = 50

	# default damage multiplier
	multiplier_vs_category = {}

	def __init__(self, weapon_type):
		self.weapon_type = weapon_type

	# returns the default multiplier vs. an unit category
	def get_default_multiplier(self, weapon_type):
		multiplier = None
		# SWORD
		if weapon_type == WeaponType.WEAPON_SWORD:
			multiplier = {
				UnitCategory.UNIT_INFANTRY: 1,
				UnitCategory.UNIT_HEAVYINFANTRY: 0.5,
				UnitCategory.UNIT_CAVALERY: 0.4,
				UnitCategory.UNIT_MACHINE: 0.8}
		# SPEAR
		elif weapon_type == WeaponType.WEAPON_SPEAR:
			multiplier = {
				UnitCategory.UNIT_INFANTRY: 0.4,
				UnitCategory.UNIT_HEAVYINFANTRY: 0.6,
				UnitCategory.UNIT_CAVALERY: 1,
				UnitCategory.UNIT_MACHINE: 1}
		# BOW
		elif weapon_type == WeaponType.WEAPON_BOW:
			multiplier = {
				UnitCategory.UNIT_INFANTRY: 1,
				UnitCategory.UNIT_HEAVYINFANTRY: 0.4,
				UnitCategory.UNIT_CAVALERY: 0.6,
				UnitCategory.UNIT_MACHINE: 0.2}
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
