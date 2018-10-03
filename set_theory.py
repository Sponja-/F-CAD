from elements import Constant, Operation, BinaryOperation
from itertools import product, permutations, combinations

class Set(Constant):
	def __init__(self, elems):
		self.value = set(elems)

class Union(BinaryOperation):
	def __init__(self, set_1, set_2):
		operation = lambda x, y: x | y
		super().__init__(operation, set_1, set_2, symbol='|')

class Intersection(BinaryOperation):
	def __init__(self, set_1, set_2):
		operation = lambda x, y: x & y
		super().__init__(operation, set_1, set_2, symbol='&')

class Difference(BinaryOperation):
	def __init__(self, set_1, set_2):
		operation = lambda x, y: x - y
		super().__init__(operation, set_1, set_2, symbol='-')

class SymmetricDifference(BinaryOperation):
	def __init__(self, set_1, set_2):
		operation = lambda x, y: x ^ y
		super().__init__(operation, set_1, set_2, symbol='^')

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
		operation = lambda x, y: list(product(x, y))
		super().__init__(operation, set_1, set_2, symbol='x')

class Permutations(BinaryOperation):
	def __init__(self, set, length):
		operation = lambda x, y: list(permutations(x, y))
		super().__init__(operation, set, length, symbol='P')

class Combinations(BinaryOperation):
	def __init__(self, set, length):
		operation = lambda x, y: list(combinations(x, y))
		super().__init__(operation, set, length, symbol='C')

class SetBuilder(Operation):
	def __init__(self, range, condition):
		operation = lambda x, y: {x for x in range if condition(x)}
		super().__init__(operation, range, condition)

	def __str__(self):
		return r"{x | x in " + str(self.operands[0]) + " and " str(condition) "}"