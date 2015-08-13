from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from core.managers.locator import Locator

class BottomBar(BoxLayout):
	actionbutton = None
	labels = None
	heading = None
	details = None
	nextturnbutton = None

	def __init__(self, **kwargs):
		super(BottomBar, self).__init__(orientation="horizontal", padding=10, size_hint=(1, None))

		# make action button
		self.actionbutton = Button(pos=(0, 0), text="Action", size_hint=(.1, 1), on_press=Locator.GUI_MGR.button_clicked)
		self.actionbutton.tag = "ACTION"
		# make label widgets
		self.labels = BoxLayout(orientation="vertical", halign="left", valign="top", size_hint=(.8, 1))
		self.heading = Label(text="Headings", halign="left", valign="top", text_size=(400, None), size_hint=(1, .5), font_size=28)
		self.details = Label(text="Much more detailled infos", text_size=(400, None), size_hint=(1, .3), font_size=24)
		self.labels.add_widget(self.heading)
		self.labels.add_widget(self.details)
		# make next turn button
		self.nextturnbutton = Button(text="Next Turn", size_hint=(.1, 1), on_press=Locator.GUI_MGR.button_clicked)
		self.nextturnbutton.tag = "NEXTTURN"
		# add all to BottomBar
		self.add_widget(self.actionbutton)
		self.add_widget(self.labels)
		self.add_widget(self.nextturnbutton)

	def set_heading_text(self, text):
		self.heading.text = text

	def set_details_text(self, text):
		self.details.text = text

	def set_action(self, text):
		self.actionbutton.text = text

	def get_action(self):
		return self.actionbutton.text