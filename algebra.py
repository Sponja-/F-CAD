from elements import Element, BinaryOperation, Operation, Constant
from arithmetic import Addition
from numpy import array, arange, sum

class Vector(Element):
	def __init__(self, elems, **kwargs):
		self.value = array(elems)
		super().__init__(**kwargs)

	def eval(self):
		return self.value

	def __str__(self):
		return str(self.value)

class Range(Operation):
	def __init__(self, start, end, step=1):
		operation = lambda start, end, step: arange(start, end, step)
		super().__init__(operation, start, end, step)

	def __str__(self):
		return f"({str(self.operands[0])}, {str(self.operands[0] + self.operands[2])} ... {str(self.operands[1])})"

class Subscript(Operation):
	def __init__(self, operand_1, operand_2):
		operation = lambda x, y: x[y]
		super().__init__(operation, operand_1, operand_2)

	def __str__(self):
		return f"{str(self.operands[0])}[{str(self.operands[1])}]"

class DotProduct(BinaryOperation):
	def __init__(self, operand_1, operand_2):
		operation = lambda x, y: sum(x * y)
		super().__init__(operation, operand_1, operand_2, symbol='.')

class Magnitude(Operation):
	def __init__(self, operand):
		operation = lambda x: sum(x ** 2) ** 0.5
		super().__init__(operation, operand)

	def __str__(self):
		return f"|{str(self.operands[0])}|"

class Sumation(Operation):
	def __init__(self, term):
		operation = lambda x: sum(x)
		super().__init__(operation, term, symbol="sum")
