from elements import Operation

class Print(Operation):
	def __init__(self, operand):
		operation = print
		super().__init__(operation, operand)