import os

# static class for accessing game paths and os methods
class FileManager(object):
	_initialized = False
	game_root = ""
	img_basepath = ""
	mods_basepath = ""

	# set the game root folder path
	@classmethod
	def set_game_root(self, path):
		self.game_root = path
		self.img_basepath = path + "/img/"
		self.mods_basepath = path + "/mods/"
		self._initialized = True

	# check if the FileManager is already initialized with set_game_root()
	@classmethod
	def check_if_initialized(self):
		if not self._initialized:
			return

	# returns the games root foldervpath
	@classmethod
	def game_root(self):
		self.check_if_initialized()
		return self.game_root

	# returns the image resource folder path
	@classmethod
	def image_path(self):
		self.check_if_initialized()
		return self.img_basepath

	# returns the mod folder path
	@classmethod
	def mod_path(self):
		self.check_if_initialized()
		return self.mods_basepath

	# open a file and return it's content
	@classmethod
	def read_file(self, file_path):
		content = ""
		file = open(file_path, "r")
		content = file.read()
		file.close()
		return content
