from elements import Constant, classes_for_values, Operation

class String(Constant):
	def __init__(self, value):
		self.value = value

classes_for_values[str] = String

class CharToCode(Operation):
	def __init__(self, char):
		operation = ord
		super().__init__(operation, char)

class CodeToChar(Operation):
	def __init__(self, number):
		operation = lambda x: chr(int(x))
		super().__init__(operation, char)