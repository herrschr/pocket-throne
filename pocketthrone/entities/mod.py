__all__ = "Mod"

from pocketthrone.managers.filemanager import FileManager

class Mod:
	# engine identifiers
	_id = -1
	_tag = "[Mod] "
	_basename = None

	# entity strings
	name = None
	desc = ""
	desc_de = ""
	author = ""

	# entity flags
	is_initialized = False
	is_disabled = False
	is_empty = False

	def __init__(self, basename, name="<nameless>", desc="", desc_de=None, disabled=False, author="unknown"):
		# set optional properties OR defaults
		self._basename = basename
		self.author = author
		self.is_disabled = disabled
		self.name = name
		# descriptions
		self.desc = desc
		self.desc_de = desc_de
		# file paths
		self.json_path = None
		self.folder_path = None
		# initialize
		self.initialize()

	def initialize(self):
		# make absolute mod .json file path
		folder_path = FileManager.mod_path() + self._basename
		json_path =  folder_path + "/" + self._basename + ".json"
		# update entity-wide
		self.folder_path = folder_path
		self.json_path = json_path
		# warn when no German translation is found
		if not self.desc_de:
			self.desc_de = "<DE>" + self.desc
		# flag mod as initialized
		self.is_initialized = True

	# returns if the Mod is allowed to select
	def allowed(self):
		if self.is_initialized and self.is_enabled():
			return True
		return False

	# set the mod as enabled
	def set_enabled(self):
		self.is_disabled = False

	# set the mod as disabled
	def set_disabled(self):
		self.is_disabled = True

	# returns if the mod is enabled
	def is_enabled(self):
		return not self.is_disabled

	# returns if the mod is disabled
	def is_disabled(self):
		return self.is_disabled

	# returns the human readable Mod name
	def get_name(self):
		if not self.allowed():
			return "<uninitialized>"
		return self.name

	# returns the Mods author
	def get_author(self):
		return self.author

	def validate(self):
		self.is_valid = True

	# returns a human readable comprehension of this Mod entity
	def __repr__(self):
		return "<Mod basename=" + self._basename + " name=" + self.get_name() + " allowed=" + str(self.allowed()) + ">"