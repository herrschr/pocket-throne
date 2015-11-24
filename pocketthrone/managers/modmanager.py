__all__ = ('ModManager')

import os
import json

from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.unitmanager import UnitManager
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.entities.event import *

from pocketthrone.managers.locator import Locator
from pocketthrone.managers.filemanager import FileManager
from pocketthrone.managers.eventmanager import EventManager
from pocketthrone.entities.event import *
from pocketthrone.entities.mod import Mod

class ModManager:
	_tag = "[ModManager] "
	# primary Mod collection holder
	mods = []
	mods_by_name = {}
	_last_mod_id = -1
	# manager flags
	selected_mod = None
	is_initialized = False

	def __init__(self, mod_name="base"):
		self.load_mods()
		self.set_selected_mod(mod_name)
		self.is_initialized = True

	# returns a new, unused mod id
	def next_mod_id(self):
		self._last_mod_id += 1
		return self._last_mod_id

	# load mod collection from disk
	def load_mods(self):
		# make function-wide collections
		subfolder_names = []
		mod_list = []
		mod_list_by_name = {}

		# iterate through folder names in $APPROOT/mods/ for overview
		for foldername in os.listdir(FileManager.mod_path()):
			subfolder_names.append(foldername)
			print(self._tag + "mod folder name " + foldername)

		# iterate through folder names in $APPROOT/mods/ for Mod loading
		for basename in subfolder_names:
			# make Mod entity & set id
			mod = self.get_mod(basename)
			mod._id = self.next_mod_id()
			# append Mod to holder collections
			self._add_mod(mod)

		# save Mod collections
		self.mods = mod_list
		self.mods_by_name = mod_list_by_name

	# load a single mod from disk by mod basename
	def get_mod(self, basename):
		# load json from basename.json file
		json_file_path = FileManager.mod_path() + basename + "/" + basename + ".json"
		mod_json_content = FileManager.read_file(json_file_path)
		mod = Mod(basename, disabled=True)
		# make empty properties
		mod_name = None
		mod_author = None
		mod_desc = None
		mod_disabled = False
		# mod is a dummy
		if not mod_json_content:
			mod.is_empty = True
			return mod;
		# load Mod properties from json
		mod_json = json.loads(mod_json_content)
		mod_name = mod_json.get("name", "<unnamed>")
		mod_author = mod_json.get("author", "<unauthorized>")
		mod_desc = mod_json.get("desc", "<missing description>")
		mod_disabled = mod_json.get("disabled", False)
		# make new Mod entity
		mod = Mod(basename, name=mod_name, desc=mod_desc, author=mod_author, disabled=mod_disabled)
		# return created Mod instance
		return mod

	# add a mod entity to ModManager
	def _add_mod(self, mod):
		self.mods.append(mod)
		self.mods_by_name[mod._basename] = mod
		print(self._tag + "mod ADDED " + repr(mod))

	def add_mod(self, basename, name, desc="", desc_de=None):
		mod = Mod(basename, name=name, desc=desc, desc_de=desc_de)
		self._add_mod(mod)

	# returns Mod entity list when initialized
	def get_mods(self):
		if self.is_initialized:
			return self.mods
		else:
			return None

	# return selected Mod in this
	def get_selected_mod(self):
		return self.selected_mod

	# select a Mod by basename
	def set_selected_mod(self, basename):
		self.selected_mod = self.get_mod(basename)
		print(self._tag + "selected mod is now " + repr(self.get_selected_mod()))
