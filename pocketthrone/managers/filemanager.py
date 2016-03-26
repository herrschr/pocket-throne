__all__ = ['FileManager']

import os
from kivy.core.image import Image as CoreImage
from kivy.cache import Cache

# static class for accessing game paths and os methods
class FileManager:
	_tag = "[FileManager] "
	_initialized = False
	IMAGE_FORMAT = ".png"

	# to be set diectly after creation
	root = {"game": None, "img": None, "mod": None}

	# texture cache
	TEXTURE_CACHE = "textures"
	_texture_none = None

	@classmethod
	def set_game_root(self, path):
		'''sets the game folder paths considering root path'''
		self.root["game"] = path
		self.root["img"] = path + "/img/"
		self.root["mod"] = path + "/mods/"
		self.initialize()

	@classmethod
	def initialize(self):
		'''flag FileManager as initialized'''
		# make texture cache
		Cache.register(self.TEXTURE_CACHE)
		# flag FileManager as initialized
		self._initialized = True

	@classmethod
	def check_if_initialized(self):
		'''aborts method if manager is uninitialized'''
		if not self._initialized:
			return False

	@classmethod
	def game_root(self):
		'''returns root doler path'''
		self.check_if_initialized()
		return self.root["game"]

	@classmethod
	def img_root(self):
		'''returns the image resource folder path'''
		self.check_if_initialized()
		return self.root["img"]

	@classmethod
	def img_format(self):
		'''returns accepted image file extension'''
		return ".png"

	@classmethod
	def mod_root(self):
		'''returns the mod folder path'''
		self.check_if_initialized()
		return self.root["mod"]

	@classmethod
	def exists(self, file_name, is_image=False, auto_ext=True):
		'''returns whether a file exists'''
		if is_image:
			file_path = self.img_root() + file_name
			if auto_ext:
				file_path += ".png"
			return os.path.isfile(file_path)
		return os.path.isfile(file_name)

	@classmethod
	def read_file(self, file_path):
		'''returns content of file under path file_path'''
		print(self._tag + "READ " + file_path)
		content = ""
		file = open(file_path, "r")
		content = file.read()
		file.close()
		return content

	@classmethod
	def get_texture(self, name, type="", use_cache=True):
		'''returns a kivy Texture loaded from'''
		# argument rel_path is relative this games image directory
		texture = None
		# when manager is uninitialized
		if not self._initialized:
			print(self._tag + "ERROR manager is not initialized")
			return None
		# when parameter rel_path is None -> return default texture
		elif name == None or name == "none":
			print(self._tag + "ERROR while loading texture; is none.")
			return
		# when manager is initialized AND rel_path =/= None OR "none"
		elif use_cache == True:
			return self.get_texture_from_cache(name)

		elif use_cache == False:
			return self.get_texture_from_file(name)


	@classmethod
	def get_texture_from_file(self, name):
		'''returns texture class from file name'''
		full_name = str(name) + ".png"
		abs_path = self.img_root() + full_name
		texture = None
		try:
			if abs_path:
				print(self._tag + "trying to load " + str(abs_path) + " from file")
				image = CoreImage(abs_path)
				if image:
					texture = image.texture
		except:
			print(self._tag + "ABORT; can't load texture")
			return
		return texture

	@classmethod
	def add_texture_to_cache(self, name):
		'''ads a texture to texture cache'''
		texture = self.get_texture_from_file(name)
		Cache.append(self.TEXTURE_CACHE, name, texture)

	@classmethod
	def get_texture_from_cache(self, name):
		'''returns a texture under name from cache'''
		#try to load texture from cache
		texture = Cache.get(self.TEXTURE_CACHE, name)
		if texture != None:
			return texture
		if texture == None:
			# load from file & add to cache
			texture = self.get_texture_from_file(name)
			self.add_texture_to_cache(name)
		# return texture
		return texture
