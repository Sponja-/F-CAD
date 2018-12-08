from elements import Constant, Operation, BinaryOperation, type_functions
from numpy import array

class Set(Operation):
	def __init__(self, *elems):
		def operation(*elems):
			return set(elems)
		super().__init__(operation, *elems)

	def __str__(self):
		return '{' + ', '.join(str(operand) for operand in self.operands) + '}'

type_functions[set] = Set

class Union(BinaryOperation):
	def __init__(self, set_1, set_2):
		operation = lambda x, y: x | y
		super().__init__(operation, set_1, set_2, symbol='|')

class Intersection(BinaryOperation):
	def __init__(self, set_1, set_2):
		operation = lambda x, y: x & y
		super().__init__(operation, set_1, set_2, symbol='&')

class IsSubset(BinaryOperation):
	def __init__(self, set_1, set_2):
		operation = lambda x, y: x <= y
		super().__init__(operation, set_1, set_2, symbol='<=')

class IsSuperset(BinaryOperation):
	def __init__(self, set_1, set_2):
		operation = lambda x, y: x >= y
		super().__init__(operation, set_1, set_2, symbol='>=')

class Contains(BinaryOperation):
	def __init__(self, value, set):
		operation = lambda x, y: x in y
		super().__init__(operation, value, set, symbol="in")