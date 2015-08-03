from core.app import PocketLordApp
from kivy.core.window import Window
from kivy.config import Config

Config.set("graphics", "width", 1000)
Config.set("graphics", "height", 800)
PocketLordApp().run()