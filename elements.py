from itertools import zip_longest

class Constant:
	def eval(self):
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

	def eval(self):
		return Variable.table[self.symbol].eval()

	@property
	def value(self):
		return Variable.table[self.symbol]

	@value.setter
	def value(self, val):
		Variable.table[self.symbol] = val

	def __str__(self):
		return self.symbol

class temp_vars:
	def __init__(self, **kwargs):
		self.vars = kwargs
	
	def __enter__(self, **kwargs):
		self.prev_values = {key: Variable.table.get(key, None) for key in self.vars.keys()}
		for key, value in self.vars.items():
			Variable.table[key] = value
		
	def __exit__(self, type, value, tb):
		for key in self.vars.keys():
			prev_value = self.prev_values[key]
			if prev_value is not None:
				Variable.table[key] = prev_value
			else:
				del Variable.table[key]			

class Operation:
	def __init__(self, operation, *operands, **kwargs):
		self.symbol = kwargs.get("symbol", self.__class__.__name__)
		self.operation = operation
		self.operands = operands

	def eval(self):
		return self.operation(*(op.eval() for op in self.operands))

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

class FunctionCall(Operation):
	def __init__(self, function, *args):
		def operation(x, *y):
			with temp_vars(**{key: val for key, val in zip_longest(x.symbols, y, fillvalue=None)}):
				return x.operation.eval()
		super().__init__(operation, function, *args)

	def eval(self):
		return self.operation(self.operands[0].eval(), *self.operands[1:])

	def __str__(self):
		return f"{str(self.operands[0])}({', '.join(str(op) for op in self.operands[1:])})"

def assign(var, value):
	if type(var) is Variable:
		var.value = value