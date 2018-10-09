import kivy
kivy.require("1.10.1")
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from editable_label import EditableLabel


class Element(BoxLayout):
	pass

class TextElement(Element):
	pass

class Formula(Widget):
	pass

class FCAD(App):
	def build(self):
		return Formula()

if __name__ == '__main__':
	FCAD().run()