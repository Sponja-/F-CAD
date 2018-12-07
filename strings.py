from elements import Constant, type_functions, Operation
from numpy import str_

class String(Constant):
	def __init__(self, value):
		self.value = value

type_functions[str] = String
type_functions[str_] = String

class CharToCode(Operation):
	def __init__(self, char):
		operation = ord
		super().__init__(operation, char)

class CodeToChar(Operation):
	def __init__(self, number):
		operation = lambda x: chr(int(x))
		super().__init__(operation, char)

class ToNumber(Operation):
	def __init__(self, string):
		operation = lambda x: float(x)
		super().__init__(operation, string)