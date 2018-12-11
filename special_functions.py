from elements import Operation, Variable, Function, type_functions, convert_type

"""

	I/O

"""

class Show(Operation):
	def __init__(self, operand):
		if type(operand) is Variable:
			operation = lambda x: print(str(x.get_value()))
		else:
			operation = lambda x: print(str(x))
		super().__init__(operation, operand, symbol="show")

	def eval(self, **locals):
		self.operation(self.operands[0])
		return self.operands[0].eval(**locals)

"""

	Language Integration

"""

class RunPython(Operation):
	def __init__(self, code):
		def operation(x):
			l = {}
			exec(x, {}, l)
			for name, value in l.items():
				if type(value) in type_functions:
					Variable.table[name] = convert_type(value)
		super().__init__(operation, code)