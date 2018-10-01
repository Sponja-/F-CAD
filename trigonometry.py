from elements import Operation, BinaryOperation
import numpy as np

class Sine(Operation):
	def __init__(self, operand):
		operation = np.sin
		super().__init__(operation, operand, symbol="sin")

class Cosine(Operation):
	def __init__(self, operand):
		operation = np.cos
		super().__init__(operation, operand, symbol="cos")

class Tangent(Operation):
	def __init__(self, operand):
		operation = np.tan
		super().__init__(operation, operand, symbol="cos")

class ArcSine(Operation):
	def __init__(self, operand):
		operation = np.arcsin
		super().__init__(operation, operand, symbol="arcsin")

class ArcCosine(Operation):
	def __init__(self, operand):
		operation = np.arccos
		super().__init__(operation, operand, symbol="arccos")

class ArcTangent(Operation):
	def __init__(self, operand):
		operation = np.arctan
		super().__init__(operation, operand, symbol="arctan")