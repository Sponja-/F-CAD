from elements import Operation, BinaryOperation, Constant
from constants import e

__ten = Constant(10)
__two = Constant(2)

class Addition(BinaryOperation):
	def __init__(self, number_1, number_2):
		operation = lambda x, y: x + y
		super().__init__(operation, number_1, number_2, symbol='+')

class Substraction(BinaryOperation):
	def __init__(self, number_1, number_2):
		operation = lambda x, y: x - y
		super().__init__(operation, number_1, number_2, symbol='-')

class Multiplication(BinaryOperation):
	def __init__(self, number_1, number_2):
		operation = lambda x, y: x * y
		super().__init__(operation, number_1, number_2, symbol='*')

class Division(BinaryOperation):
	def __init__(self, number_1, number_2):
		operation = lambda x, y: x / y
		super().__init__(operation, number_1, number_2, symbol='/')

class Exponentation(BinaryOperation):
	def __init__(self, number_1, number_2):
		operation = lambda x, y: x ** y
		super().__init__(operation, number_1, number_2, symbol='^')

class SquareRoot(Operation):
	def __init__(self, number):
		operation = lambda x: x ** 0.5
		super().__init__(operation, number, symbol="sqrt")

class NthRoot(BinaryOperation):
	def __init__(self, number_1, number_2):
		operation = lambda x, y: x ** (1 / y)
		super().__init__(operation, number_1, number_2)

	def __str__(self):
		return f"{str(self.operands[1])}-rt({str(self.operands[0])})"

class Logarithm(BinaryOperation):
	def __init__(self, number_1, number_2):
		operation = lambda x, y: np.log(number_1) / np.log(number_2)
		super().__init__(operation, number_1, number_2)
	
	def __str__(self):
		return f"log({self.operands[0]}, base={self.operands[1]})"

class CommonLogarithm(Logarithm):
	def __init__(self, number):
		super().__init__(number, __ten)

	def __str__(self):
		return f"log({self.operands[0]})"

class LogarithmBase2(Logarithm):
	def __init__(self, number):
		super().__init__(number, __two)

	def __str__(self):
		return f"lg({self.operands[0]})"

class LogarithmBaseE(Logarithm):
	def __init__(self, number):
		super().__init__(number, e)

	def __str__(self):
		return f"ln({self.operands[0]})"

class Modulo(BinaryOperation):
	def __init__(self, number_1, number_2):
		operation = lambda x, y: x % y
		super().__init__(operation, number_1, number_2, symbol='%')

class Opposite(Operation):
	def __init__(self, number):
		operation = lambda x: -x
		super.__init__(operation, number, symbol="-")

class Inverse(Operation):
	def __init__(self, number):
		operation = lambda x: 1 / x
		super.__init__(operation, number)

	def __str__(self):
		return f"({str(self.operands[0])}^-1)"

class AbsoluteValue(Operation):
	def __init__(self, number):
		operation = lambda x: (x ** 2) ** 0.5 
		super().__init__(operation, number, symbol='abs')