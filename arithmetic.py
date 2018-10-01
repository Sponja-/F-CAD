from elements import Operation, BinaryOperation, Constant

class Addition(BinaryOperation):
	def __init__(self, operand_1, operand_2):
		operation = lambda x, y: x + y
		super().__init__(operation, operand_1, operand_2, symbol='+')

class Substraction(BinaryOperation):
	def __init__(self, operand_1, operand_2):
		operation = lambda x, y: x - y
		super().__init__(operation, operand_1, operand_2, symbol='-')

class Multiplication(BinaryOperation):
	def __init__(self, operand_1, operand_2):
		operation = lambda x, y: x * y
		super().__init__(operation, operand_1, operand_2, symbol='*')

class Division(BinaryOperation):
	def __init__(self, operand_1, operand_2):
		operation = lambda x, y: x / y
		super().__init__(operation, operand_1, operand_2, symbol='/')

class Exponentation(BinaryOperation):
	def __init__(self, operand_1, operand_2):
		operation = lambda x, y: x ** y
		super().__init__(operation, operand_1, operand_2, symbol='^')

class NthRoot(BinaryOperation):
	def __init__(self, operand_1, operand_2):
		operation = lambda x, y: x ** (1 / y)
		super().__init__(operation, operand_1, operand_2)

	def __str__(self):
		return f"{str(self.operands[1])}-rt({str(self.operands[0])})"

class Logarithm(BinaryOperation):
	def __init__(self, operand_1, operand_2):
		operation = lambda x, y: np.log(operand_1) / np.log(operand_2)
		super().__init__(operation, operand_1, operand_2)
	
	def __str__(self):
		return f"log({', '.join(str(op) for op in self.operands)})"

class Modulo(BinaryOperation):
	def __init__(self, operand_1, operand_2):
		operation = lambda x, y: x % y
		super().__init__(operation, operand_1, operand_2, symbol='%')

class Negation(Operation):
	def __init__(self, operand):
		operation = lambda x: -x
		super.__init__(operation, operand, symbol="-")

class Inversion(Operation):
	def __init__(self, operand):
		operation = lambda x: 1 / x
		super.__init__(operation, operand)

	def __str__(self):
		return f"({str(self.operands[0])})^-1"

class AbsoluteValue(Operation):
	def __init__(self, operand):
		operation = lambda x: (x ** 2) ** 0.5 
		super().__init__(operation, operand, symbol='abs')