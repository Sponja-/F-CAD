from elements import Operation, BinaryOperation

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

class Exponentiation(BinaryOperation):
	def __init__(self, number_1, number_2):
		operation = lambda x, y: x ** y
		super().__init__(operation, number_1, number_2, symbol='^')

class Modulo(BinaryOperation):
	def __init__(self, number_1, number_2):
		operation = lambda x, y: x % y
		super().__init__(operation, number_1, number_2, symbol='%')

class Opposite(Operation):
	def __init__(self, number):
		operation = lambda x: -x
		super().__init__(operation, number, symbol="-")

class Inverse(Operation):
	def __init__(self, number):
		operation = lambda x: 1 / x
		super().__init__(operation, number, symbol="inv")