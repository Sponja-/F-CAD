import kivy
kivy.require("1.10.1")
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

class FCAD(App):
	def build(self):
		return Label(text="FCAD")

if __name__ == '__main__':
	FCAD().run()