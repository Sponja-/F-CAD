from elements import *
from importlib import import_module
from types import FunctionType, BuiltinFunctionType
from numpy import ufunc

class class_value:
	def __init__(self, name, parent, attributes):
		self.name = name
		self.parent = parent
		for name, value in attributes.items():
			setattr(self, name, value)

class Class(Constant):
	table = {}

	def __init__(self, name, parent, attributes):
		self.value = class_value(name, parent, attributes)
		Class.table[name] = self.value

class ClassDefinition(Operation):
	def __init__(self, name, parent, attributes):
		def operation(x, y, z):
			Variable.table[x] = Class(x, y, z)
			return Variable.table[x]
		super().__init__(operation, non_eval_operands=[name, parent, attributes])

forbidden = [
	'__class__',
	'__delattr__',
	'__dict__',
	'__dir__',
	'__getattribute__',
	'__init__',
	'__init_subclass__',
	'__module__',
	'__new__',
	'__reduce__',
	'__reduce_ex__',
	'__setattr__',
	'__sizeof__',
	'__subclasshook__',
	'__weakref__'
]

class instance:
	def __init__(self, class_name):
		cls = Class.table[class_name]
		self.__class_name__ = class_name
		for attr_name in dir(cls):
			if attr_name not in forbidden:
				setattr(self, attr_name, getattr(cls, attr_name))
		self.__instance_attributes__ = {}

class Instance(Constant):
	def __init__(self, value):
		self.value = value

type_functions[instance] = Instance
type_functions[class_value] = Class

class ImportedOperation(Operation):
	def eval(self, **locals):
		return self.operation(*locals["args"].eval(**locals))

class ImportedClass(Constant):
	def __init__(self, python_class):
		pass

function_types = [
	FunctionType,
	BuiltinFunctionType,
	ufunc
]

def import_value(value):
	if type(value) in type_functions.keys():
		return convert_type(value)
	elif type(value) in function_types:
		return Function([], ImportedOperation(value), "args")

class ImportPythonModule(Operation):
	def __init__(self, module_name):
		def operation(x):
			module = import_module(x)
			for var_name in dir(module):
				if not (var_name.startswith("__") and var_name.endswith("__")):
					Variable.table[var_name] = import_value(getattr(module, var_name)) 
		super().__init__(operation, module_name)

class MethodCall(FunctionCall):
	def __init__(self, inst, function, *args):
		self.inst = inst
		super().__init__(function, *args)

	def eval(self, **locals):
		new_locals = locals.copy()
		this = self.inst
		if(type(this) is Variable):
			this = this.get_value(**locals)
		new_locals["this"] = this
		return super().eval(**new_locals)

class CreateInstance(Operation):
	def __init__(self, class_name, *params):
		self.class_name = class_name
		self.params = params

	def eval(self, **locals):
		inst = instance(self.class_name)
		MethodCall(Instance(inst), inst.constructor, *self.params).eval(**locals)
		return inst

class AccessMember:
	def __init__(self, inst, attr_name):
		self.inst = inst
		self.attr_name = attr_name

	def get_value(self, **locals):
		value = self.inst.eval(**locals)
		if self.attr_name in value.__instance_attributes__.keys():
			return value.__instance_attributes__[self.attr_name]
		else:
			return getattr(value, self.attr_name)

	def set_value(self, value, **locals):
		self.inst.eval(**locals).__instance_attributes__[self.attr_name] = value

	def eval(self, **locals):
		return self.get_value(**locals).eval(**locals)

	def __str__(self):
		return f"{str(self.inst)}.{self.attr_name}"