from core.app import PocketThroneApp
from kivy.core.window import Window
from kivy.config import Config
import cProfile

Config.set("graphics", "width", 1000)
Config.set("graphics", "height", 800)

#cProfile.run('PocketThroneApp().run()')
PocketThroneApp().run()
