from elements import Operation, Variable, Function, type_functions, convert_type
from importlib import import_module
from types import FunctionType, BuiltinFunctionType
from numpy import ufunc

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

class ImportedOperation(Operation):
	def eval(self, **locals):
		return self.operation(*locals["args"].eval(**locals))

function_types = [
	FunctionType,
	BuiltinFunctionType,
	ufunc
]

class ImportPythonModule(Operation):
	def __init__(self, module_name):
		def operation(x):
			module = import_module(x)
			for var_name in dir(module):
				if not (var_name.startswith("__") and var_name.endswith("__")):
					value = getattr(module, var_name) 
					if type(value) in type_functions.keys():
						Variable.table[var_name] = convert_type(value)
					elif type(value) in function_types:
						Variable.table[var_name] = Function([], ImportedOperation(value), "args")
		super().__init__(operation, module_name)