from abc import abstractmethod

var_table = {}

class Element:
	def __init__(self, **kwargs):
		pass

	@abstractmethod
	def eval(self):
		return None

	@abstractmethod
	def __str__(self):
		return ""

class Constant(Element):
	def __init__(self, value, **kwargs):
		self.value = value
		super().__init__(**kwargs)

	def eval(self):
		return self.value

	def __str__(self):
		return str(self.value)

class Variable(Element):
	def __init__(self, symbol, value, **kwargs):
		self.symbol = symbol
		self.value = value
		var_table[symbol] = self
		super().__init__(**kwargs)

	def eval(self):
		return self.value.eval()

	def __str__(self):
		return self.symbol
		
class Operation(Element):
	def __init__(self, operation, *operands, **kwargs):
		self.symbol = kwargs.get("symbol", self.__class__.__name__)
		self.operation = operation
		self.operands = operands
		super().__init__(**kwargs)

	def eval(self):
		return self.operation(*(op.eval() for op in self.operands))

	def __str__(self):
		return f"{self.symbol}({', '.join(str(op) for op in self.operands)})"

class BinaryOperation(Operation):
	def __init__(self, operation, operand_1, operand_2, **kwargs):
		super().__init__(operation, operand_1, operand_2, **kwargs)

	def __str__(self):
		return f"({str(self.operands[0])} {self.symbol} {str(self.operands[1])})"
