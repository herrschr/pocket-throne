__all__ = "Mod"

from pocketthrone.managers.filemanager import FileManager

class Mod:
	# engine identifiers
	_id = -1
	_tag = "[Mod] "
	basename = None

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
		self.basename = basename
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
		'''initializes mod entity'''
		# make absolute mod .json file path
		folder_path = FileManager.mod_root() + self.basename
		json_path =  folder_path + "/" + self.basename + ".json"
		# update entity-wide
		self.folder_path = folder_path
		self.json_path = json_path
		# warn when no German translation is found
		if not self.desc_de:
			self.desc_de = "<DE>" + self.desc
		# flag mod as initialized
		self.is_initialized = True

	def allowed(self):
		'''returns whether this mod is initialized'''
		if self.is_initialized and self.is_enabled():
			return True
		return False

	def set_enabled(self):
		'''flags this mod as enabled'''
		self.is_disabled = False

	def set_disabled(self):
		'''flags this mod as disabled'''
		self.is_disabled = True

	def is_enabled(self):
		'''returns whether this mod is enabled'''
		return not self.is_disabled

	def is_disabled(self):
		'''returns whether this mod is disabled'''
		return self.is_disabled

	def get_name(self):
		'''returns english mod name'''
		if not self.allowed():
			return "<uninitialized>"
		return self.name

	def get_author(self):
		'''returns mod author name'''
		return self.author

	def validate(self):
		'''flags mod as validated'''
		self.is_valid = True

	def __repr__(self):
		'''returns xml like mod representation'''
		return "<Mod basename=" + self.basename + " name=" + self.get_name() + " allowed=" + str(self.allowed()) + ">"
