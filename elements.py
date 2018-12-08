from itertools import zip_longest
from numpy import float64
from pprint import pprint
from numpy import array, ndarray

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
		return self.get_value()

	@value.setter
	def value(self, val):
		self.set_value(val)

	def get_value(self, **locals):
		return Variable.table[self.symbol]

	def set_value(self, value, **locals):
		Variable.table[self.symbol] = value

	def __str__(self):
		return self.symbol

class Operation:
	def __init__(self, operation, *operands, **kwargs):
		self.symbol = kwargs.get("symbol", self.__class__.__name__)
		self.operation = operation
		self.operands = list(operands)

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
	def __init__(self, var_symbols, var_arg_symbol, operation):
		self.symbols = var_symbols
		self.var_arg_symbol = var_arg_symbol
		self.operation = operation

	def __str__(self):
		return str(self.operation)

class Function(Constant):
	def __init__(self, var_symbols, operation, var_arg_symbol=None):
		self.value = func(var_symbols, var_arg_symbol, operation)

class Vector(Operation):
	def __init__(self, *elems):
		def operation(*x):
			return array(x)
		super().__init__(operation, *elems)

type_functions = {
	int: Number,
	float: Number,
	float64: Number,
	bool: Number,
	func: lambda x: Function(x.symbols, x.operation, x.var_arg_symbol)
}

def convert_type(value):
	return type_functions[type(value)](value)

type_functions[ndarray] = lambda x: Vector(*(convert_type(elem) for elem in x))
type_functions[list] = type_functions[ndarray]

class ret_val:
	def __init__(self, value):
		self.value = value

type_functions[ret_val] = lambda x: type_functions[x.value]

class expanded_vector:
	def __init__(self, value):
		self.value = value

class ExpandVector(Operation):
	def __init__(self, v):
		operation = expanded_vector
		super().__init__(operation, v)

class FunctionCall(Operation):
	def __init__(self, function, *args):
		def operation(x, locals, *y):
			new_locals = locals.copy()
			for i, arg in enumerate(y):
				value = arg.eval(**locals)
				if type(arg) is ExpandVector:
					y = y[:i] + tuple(convert_type(elem) for elem in arg.eval(**locals).value) + y[i + 1:]
			for symbol, expr in zip(x.symbols, y):
				new_locals[symbol] = convert_type(expr.eval(**new_locals))
			if x.var_arg_symbol is not None:
				new_locals[x.var_arg_symbol] = []
				for expr in y[len(x.symbols):]:
					new_locals[x.var_arg_symbol].append(convert_type(expr.eval(**new_locals)))
				new_locals[x.var_arg_symbol] = Vector(*new_locals[x.var_arg_symbol])
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