class Constant:
	def eval(self):
		return self.value

	def __str__(self):
		return str(self.value)

class Number(Constant):
	def __init__(self, value):
		self.value = value

class Variable:
	def __init__(self, symbol, value):
		self.symbol = symbol
		self.value = value

	def eval(self):
		return self.value.eval()

	def __str__(self):
		return self.symbol

class Operation:
	def __init__(self, operation, *operands):
		self.symbol = kwargs.get("symbol", self.__class__.__name__)
		self.operation = operation
		self.operands = operands

	def eval(self):
		return self.operation(*(op.eval() for op in self.operands))

	def __str__(self):
		return f"{self.symbol}({', '.join(str(op) for op in self.operands)})"

class BinaryOperation(Operation):
	def __init__(self, operation, operand_1, operand_2):
		super().__init__(operation, operand_1, operand_2)

	def __str__(self):
		return f"({str(self.operands[0])} {self.symbol} {str(self.operands[1])})"
