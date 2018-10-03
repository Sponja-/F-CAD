from elements import Operation, BinaryOperation

class Conjunction(BinaryOperation):
	def __init__(self, boolean_1, boolean_2):
		operation = lambda x, y: bool(x) and bool(y)
		super().__init__(operation, boolean_1, boolean_2, symbol='and')

class InclusiveDisjunction(BinaryOperation):
	def __init__(self, boolean_1, boolean_2):
		operation = lambda x, y: bool(x) or bool(y)
		super().__init__(operation, boolean_1, boolean_2, symbol='or')
	
class ExclusiveDisjunction(BinaryOperation):
	def __init__(self, boolean_1, boolean_2):
		operation = lambda x, y: bool(x) ^ bool(y)
		super().__init__(operation, boolean_1, boolean_2, symbol='xor')	

class Negation(Operation):
	def __init__(self, boolean_1):
		operation = lambda x: not bool(x)
		super().__init__(operation, boolean_1, boolean_2, symbol='not')

class Equal(BinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x == y
		super().__init__(operation, value_1, value_2, symbol='=')

class Lesser(BinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x < y
		super().__init__(operation, value_1, value_2, symbol='<')

class LesserOrEqual(BinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x <= y
		super().__init__(operation, value_1, value_2, symbol='<=')

class Greater(BinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x > y
		super().__init__(operation, value_1, value_2, symbol='>')

class GreaterOrEqual(BinaryOperation):
	def __init__(self, value_1, value_2):
		operation = lambda x, y: x >= y
		super().__init__(operation, value_1, value_2, symbol='>=')

class Any(Operation):
	def __init__(self, vector):
		operation = lambda x: x.any()
		super().__init__(operation, vector, symbol='any')

class All(Operation):
	def __init__(self, vector):
		operation = lambda x: x.all()
		super().__init__(operation, vector, symbol='all')