from itertools import zip_longest
from numpy import float64
from pprint import pprint

class Constant:
	def eval(self, **locals):
		return self.value
		
	def __str__(self):
		return str(self.value)

class Number(Constant):
	def __init__(self, value):
		self.value = value

class Variable:
	table = {}

	def __init__(self, symbol):
		self.symbol = symbol

	def eval(self, **locals):
		if self.symbol in locals.keys():
			return locals[self.symbol].eval(**locals)
		return Variable.table[self.symbol].eval(**locals)

	@property
	def value(self):
		return Variable.table[self.symbol]

	@value.setter
	def value(self, val):
		Variable.table[self.symbol] = val

	def __str__(self):
		return self.symbol

class Operation:
	def __init__(self, operation, *operands, **kwargs):
		self.symbol = kwargs.get("symbol", self.__class__.__name__)
		self.operation = operation
		self.operands = operands

	def eval(self, **locals):
		return self.operation(*(op.eval(**locals) for op in self.operands))

	def __str__(self):
		return f"{self.symbol}({', '.join(str(op) for op in self.operands)})"

class BinaryOperation(Operation):
	def __init__(self, operation, operand_1, operand_2, **kwargs):
		super().__init__(operation, operand_1, operand_2, **kwargs)

	def __str__(self):
		return f"({str(self.operands[0])} {self.symbol} {str(self.operands[1])})"

class func:
	def __init__(self, var_symbols, operation):
		self.symbols = var_symbols
		self.operation = operation

	def __str__(self):
		return str(self.operation)

class Function(Constant):
	def __init__(self, var_symbols, operation):
		self.value = func(var_symbols, operation)

classes_for_values = {
	int: Number,
	float: Number,
	float64: Number,
	bool: Number,
	func: lambda x: Function(x.symbols, x.operation)
}

class ret_val:
	def __init__(self, value):
		self.value = value

classes_for_values[ret_val] = lambda x: classes_for_values[ret_val.value]

class FunctionCall(Operation):
	def __init__(self, function, *args):
		def operation(x, locals, *y):
			new_locals = locals.copy()
			for symbol, expr in zip_longest(x.symbols, y, fillvalue=None):
				value = expr.eval(**new_locals)
				new_locals[symbol] = classes_for_values[type(value)](value)
			ret = x.operation.eval(**new_locals)
			return ret.value if type(ret) is ret_val else ret
		super().__init__(operation, function, *args)

	def eval(self, **locals):
		return self.operation(self.operands[0].eval(**locals), locals, *self.operands[1:])

	def __str__(self):
		return f"{str(self.operands[0])}({', '.join(str(op) for op in self.operands[1:])})"

class Where(Operation):
	def __init__(self, op, assignments):
		def operation(x, locals, y):
			new_locals = locals.copy()
			new_locals.update(y)
			return x.eval(**new_locals)
		super().__init__(operation, op, assignments)

	def eval(self, **locals):
		return self.operation(self.operands[0], locals, self.operands[1])