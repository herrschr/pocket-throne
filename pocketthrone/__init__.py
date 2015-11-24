import sys
import os
from pocketthrone.managers.filemanager import FileManager

print("core ini")

# get game root directory on package initialization
def getGameRoot():
	return os.path.abspath(__file__ + "/../../")

# initialize file manager
game_root = getGameRoot()
FileManager.set_game_root(game_root)
