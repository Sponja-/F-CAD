from elements import Operation
from elements import Variable
from matplotlib import pyplot as plt

class Print(Operation):
	def __init__(self, operand):
		operation = print
		super().__init__(operation, operand, symbol="print")

class Graph(Operation):
	def __init__(self, free, bound):
		def operation(x, y):
			plt.plot(x, y)
			plt.show()
		super().__init__(operation, free, bound, symbol="graph")

class Scatter(Operation):
	def __init__(self, xs, ys):
		def operation(x, y):
			plt.scatter(x, y)
			plt.show()
		super().__init__(operation, xs, ys, symbol="scatter")

class Show(Operation):
	def __init__(self, operand):
		if type(operand) is Variable:
			operation = lambda x: print(str(x.value))
		else:
			operation = lambda x: print(str(x))
		super().__init__(operation, operand, symbol="show")

	def eval(self, **locals):
		self.operation(self.operands[0])