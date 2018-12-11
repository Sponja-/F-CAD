from elements import Operation, BinaryOperation
from objects import MethodCall

# class Addition(BinaryOperation):
# 	def __init__(self, number_1, number_2):
# 		operation = lambda x, y: x + y
# 		super().__init__(operation, number_1, number_2, symbol='+')

class OperatorFunctionOperation(Operation):
	def __init__(self, function_name, *operands, **kwargs):
		self.function_name = function_name
		super().__init__(None, *operands, **kwargs)

	def eval(self, **locals):
		return MethodCall(self.operands[0], getattr(self.operands[0].eval(**locals), self.function_name), *self.operands[1:]).eval(**locals)

class BinaryOperatorFunctionOperation(OperatorFunctionOperation):
	def __init__(self, function_name, operand_1, operand_2, **kwargs):
		super().__init__(function_name, operand_1, operand_2, **kwargs)

	def __str__(self):
		return f"({str(self.operands[0])} {self.symbol} {str(self.operands[1])})"

class Addition(BinaryOperatorFunctionOperation):
	def __init__(self, operand1, operand2):
		super().__init__("__add__", operand1, operand2, symbol='+')

class Substraction(BinaryOperatorFunctionOperation):
	def __init__(self, number_1, number_2):
		super().__init__("__sub__", number_1, number_2, symbol='-')

class Multiplication(BinaryOperatorFunctionOperation):
	def __init__(self, number_1, number_2):
		super().__init__("__mul__", number_1, number_2, symbol='*')

class Division(BinaryOperatorFunctionOperation):
	def __init__(self, number_1, number_2):
		super().__init__("__div__", number_1, number_2, symbol='/')

class Exponentiation(BinaryOperatorFunctionOperation):
	def __init__(self, number_1, number_2):
		super().__init__("__pow__", number_1, number_2, symbol='^')

class Modulo(BinaryOperatorFunctionOperation):
	def __init__(self, number_1, number_2):
		super().__init__("__mod__", number_1, number_2, symbol='%')

class Opposite(OperatorFunctionOperation):
	def __init__(self, number):
		super().__init__("__neg__", number, symbol="-")

class Inverse(Operation):
	def __init__(self, number):
		super().__init__("__invert__", number, symbol="inv")