from elements import Operation
from matplotlib import pyplot as plt

class Print(Operation):
	def __init__(self, operand):
		operation = print
		super().__init__(operation, operand)

class Graph(Operation):
	def __init__(self, free, bound):
		def operation(x, y):
			plt.plot(x, y)
			plt.show()
		super().__init__(operation, free, bound)