from elements import Operation, BinaryOperation
import numpy as np

class Conjunction(BinaryOperation):
	def __init__(self, boolean_1, boolean_2):
		operation = lambda x, y: np.logical_and(x, y)
		super().__init__(operation, boolean_1, boolean_2, symbol='and')

class InclusiveDisjunction(BinaryOperation):
	def __init__(self, boolean_1, boolean_2):
		operation = lambda x, y: np.logical_or(x, y)
		super().__init__(operation, boolean_1, boolean_2, symbol='or')
	
class ExclusiveDisjunction(BinaryOperation):
	def __init__(self, boolean_1, boolean_2):
		operation = lambda x, y: np.logical_xor(x, y)
		super().__init__(operation, boolean_1, boolean_2, symbol='xor')	

class Negation(Operation):
	def __init__(self, boolean_1):
		operation = lambda x: np.logical_not(x, y)
		super().__init__(operation, boolean_1, boolean_2, symbol='not')

class ChainedBinaryOperation(BinaryOperation):
	def __init__(self, operation, value_1, value_2, **kwargs):
		super().__init__(operation, value_1, value_2, **kwargs)
		if type(self.operands[0]) == type(self):
			new_self = Conjunction(self.operands[0], type(self)(self.operands[0].operands[1], self.operands[1]))
			self.__dict__.update(new_self.__dict__) # Unsafe 

class Equal(ChainedBinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x == y
		super().__init__(operation, value_1, value_2, symbol='==')

class NotEqual(ChainedBinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x != y
		super().__init__(operation, value_1, value_2, symbol='!=')

class Lesser(ChainedBinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x < y
		super().__init__(operation, value_1, value_2, symbol='<')

class LesserOrEqual(ChainedBinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x <= y
		super().__init__(operation, value_1, value_2, symbol='<=')

class Greater(ChainedBinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x > y
		super().__init__(operation, value_1, value_2, symbol='>')

class GreaterOrEqual(ChainedBinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x >= y
		super().__init__(operation, value_1, value_2, symbol='>=')