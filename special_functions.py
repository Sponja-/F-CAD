from elements import Operation, Variable, type_functions
from matplotlib import pyplot as plt
from json import dumps, loads
from importlib import import_module
from types import FunctionType

"""

	I/O

"""

class Print(Operation):
	def __init__(self, operand):
		operation = print
		super().__init__(operation, operand, symbol="print")

class Input(Operation):
	def __init__(self):
		operation = lambda: float(input())
		super().__init__(operation)

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
		return self.operands[0].eval(**locals)


"""

	OS

"""

class Read(Operation):
	def __init__(self, file_path):
		def operation(x):
			with open(x, 'r') as file:
				return file.read()
		super().__init__(operation, file_path)

class Write(Operation):
	def __init__(self, file_path, contents):
		def operation(x, y):
			with open(x, 'w') as file:
				file.write(y)
		super().__init__(operation, file_path, contents)

class JsonEncode(Operation):
	def __init__(self, obj):
		operation = dumps
		super().__init__(operation, obj)

class JsonDecode(Operation):
	def __init__(self, s):
		operation = loads
		super().__init__(operation, s)

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
					Variable.table[name] = type_functions[type(value)](value)
		super().__init__(operation, code)

class ImportPythonModule(Operation):
	def __init__(self, module_name):
		def operation(x):
			module = import_module(x.rsplit('.', 1)[0])
			for var_name in dir(module):
				if not (var_name.startswith("__") and var_name.endswith("__")):
					value = getattr(module, var_name) 
					if type(value) in type_functions:
						Variable.table[var_name] = type_functions[type(value)](value)
					elif type(value) is FunctionType:
						Variable.table[var_name] = Function([], ImportedOperation(value), "args")
		super().__init__(operation, module_name)