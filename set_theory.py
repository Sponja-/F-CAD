from elements import Constant, Operation, BinaryOperation, type_functions
from itertools import product, permutations, combinations
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

class CartesianProduct(BinaryOperation):
	def __init__(self, set_1, set_2):
		operation = lambda x, y: array(product(x, y))
		super().__init__(operation, set_1, set_2, symbol='x')

class Permutations(BinaryOperation):
	def __init__(self, set, length):
		operation = lambda x, y: array(permutations(x, y))
		super().__init__(operation, set, length, symbol='P')

class Combinations(BinaryOperation):
	def __init__(self, set, length):
		operation = lambda x, y: array(combinations(x, y))
		super().__init__(operation, set, length, symbol='C')