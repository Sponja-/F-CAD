from elements import BinaryOperation, Operation, Constant
from constants import one

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

class Shape(Operation):
	def __init__(self, matrix):
		operation = lambda x: array(x.shape)
		super().__init__(operation, matrix, symbol='shape')