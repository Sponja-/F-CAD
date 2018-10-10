import kivy
kivy.require("1.10.1")
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from editable_label import EditableLabel
from kivy.graphics import Color, Rectangle


class Element(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size_hint = None, None
		self.orientation = "horizontal"

class TextElement(Element):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 1
		self.content = Label(text="test")
		self.add_widget(self.content)

		with self.canvas.before:
			Color(0, 1, 0, .5)
			Rectangle(pos=self.pos, size=self.size)

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			print(self.get_size())
			self.add_widget(Label)

	def get_size(self):
		return self.content.texture_size
		


class Formula(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orientation = "horizontal"
		self.cols = 1
		self.size_hint = None, None
		self.size = 100, 50

		self.content = TextElement()
		self.add_widget(self.content)

		with self.canvas.before:
			Color(1, 0, 0, 1)
			Rectangle(pos=self.pos, size=self.size)

class FCAD(App):
	def build(self):
		return Formula()

if __name__ == '__main__':
	FCAD().run()