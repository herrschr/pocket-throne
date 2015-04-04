import os

# static class for accessing game paths and os methods
class FileManager(object):
	game_root = ""
	img_basepath = ""
	mods_basepath = ""

	# set the game root folder path
	@classmethod
	def set_game_root(self, path):
		self.game_root = path
		self.img_basepath = path + "/img/"
		self.mods_basepath = path + "/mods/"

	def check_if_initialized(self):
		if (game_root == ""):
			return None

	@classmethod
	def game_root(self):
		check_if_initialized()
		return self.game_root

	# returns the image resource folder path
	@classmethod
	def image_path(self):
		check_if_initialized()
		return self.img_basepath

	# returns the mod folder path
	@classmethod
	def mod_path(self):
		check_if_initialized()
		return self.mods_basepath