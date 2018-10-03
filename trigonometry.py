from elements import Operation, BinaryOperation
import numpy as np

class Sine(Operation):
	def __init__(self, number):
		operation = np.sin
		super().__init__(operation, number, symbol="sin")

class Cosine(Operation):
	def __init__(self, number):
		operation = np.cos
		super().__init__(operation, number, symbol="cos")

class Tangent(Operation):
	def __init__(self, number):
		operation = np.tan
		super().__init__(operation, number, symbol="cos")

class ArcSine(Operation):
	def __init__(self, number):
		operation = np.arcsin
		super().__init__(operation, number, symbol="arcsin")

class ArcCosine(Operation):
	def __init__(self, number):
		operation = np.arccos
		super().__init__(operation, number, symbol="arccos")

class ArcTangent(Operation):
	def __init__(self, number):
		operation = np.arctan
		super().__init__(operation, number, symbol="arctan")