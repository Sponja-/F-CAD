from elements import *

class class_value:
	def __init__(self, name, parent, attributes):
		self.name = name
		self.parent = parent
		self.attributes = parent.attributes
		self.attributes.update(attributes)

class Class(Constant):
	table = {}	

	def __init__(self, name, parent, attributes):
		self.value = class_value(name, parent, attributes)
		Class.table[name] = self.value

class instance:
	def __init__(self, class_name):
		self.class_attributes = Class.table[name]
		self.instance_attributes = {}

class Attribute(Constant):
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name

	@property
	def value(self):
		return self.parent.eval().instance_attributes[self.name]
	 

class MethodCall(FunctionCall):
	def __init__(self, inst, function, *args):
		self.inst = inst
		super().__init__(function, *args)

	def eval(self, **locals):
		new_locals = locals.copy()
		new_locals["this"] = self.inst
		super().eval(self, **new_locals)

class CreateInstance(Operation):
	def __init__(self, class_name, *params):
		def operation(x, *y):
			inst = instance(x)
			MethodCall(inst, inst.class_attributes["constructor"], *y).eval()
			return inst
		super().__init__(operation, class_name, *params)

	def eval(self, **locals):
		return self.operation(self.operands[0], *(op.eval(**locals) for op in self.operands[1:]))

class AccessMember(Operation):
	def __init__(self, inst, name):
		operation = lambda x, y:  x.instance_attributes[y]
		super().__init__(operation, inst, anem)

	def eval(self, **locals):
		return self.operation(self.operands[0], self.operands[1])