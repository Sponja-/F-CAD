from elements import BinaryOperation, Operation, Constant, classes_for_values
from constants import one
from numpy import array, ndarray

class Vector(Constant):
	def __init__(self, elems):
		self.value = array(elems)

classes_for_values[list] = Vector
classes_for_values[ndarray] = Vector

class Subscript(Operation):
	def __init__(self, vector, index):
		operation = lambda x, y: x[int(y)]
		super().__init__(operation, vector, index)

	def __str__(self):
		return f"{str(self.operands[0])}[{str(self.operands[1])}]"

class DotProduct(BinaryOperation):
	def __init__(self, vector_1, vector_2):
		operation = lambda x, y: sum(x * y)
		super().__init__(operation, vector_1, vector_2, symbol='.')

class Magnitude(Operation):
	def __init__(self, vector):
		operation = lambda x: sum(x ** 2) ** 0.5
		super().__init__(operation, vector)

	def __str__(self):
		return f"|{str(self.operands[0])}|"

class Row(BinaryOperation):
	def __init__(self, matrix, index):
		operation = lambda x, y: x[int(y)]
		super().__init__(operation, matrix, index, symbol="row")

class Column(BinaryOperation):
	def __init__(self, matrix, index):
		operation = lambda x, y: x[:, int(y)]
		super().__init__(operation, matrix, index, symbol="col")