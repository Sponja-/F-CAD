from elements import *

class class_value:
	def __init__(self, name, parent, attributes):
		self.name = name
		self.parent = parent
		self.attributes = parent.attributes if parent is not None else {}
		self.attributes.update(attributes)

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

class instance:
	def __init__(self, class_name):
		self.cls = Class.table[class_name]
		self.attributes = {}
	
class Instance(Constant):
	def __init__(self, value):
		self.value = value

type_functions[instance] = Instance

class MethodCall(FunctionCall):
	def __init__(self, inst, function, *args):
		self.inst = inst
		super().__init__(function, *args)

	def eval(self, **locals):
		new_locals = locals.copy()
		new_locals["this"] = self.inst
		return super().eval(**new_locals)

class CreateInstance(Operation):
	def __init__(self, class_name, *params):
		def operation(x, *y):
			inst = instance(x)
			MethodCall(Instance(inst), inst.cls.attributes["constructor"], *y).eval()
			return inst
		super().__init__(operation, non_eval_operands=[class_name, *params])

class AccessMember:
	def __init__(self, inst, attr_name):
		self.inst = inst
		self.attr_name = attr_name

	def get_value(self, **locals):
		value = self.inst.eval(**locals)
		return value.attributes.get(self.attr_name, value.cls.attributes.get(self.attr_name, None))

	def set_value(self, value, **locals):
		self.inst.eval(**locals).attributes[self.attr_name] = value

	def eval(self, **locals):
		return self.get_value(**locals).eval(**locals)

