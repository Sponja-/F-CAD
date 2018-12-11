from elements import *

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

class instance:
	def __init__(self, class_name):
		self.cls = Class.table[class_name]
	
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
		MethodCall(Instance(inst), inst.cls.constructor, *self.params).eval(**locals)
		return inst

class AccessMember:
	def __init__(self, inst, attr_name):
		self.inst = inst
		self.attr_name = attr_name

	def get_value(self, **locals):
		value = self.inst.eval(**locals)
		if hasattr(value, self.attr_name):
			return getattr(value, self.attr_name)
		else:
			return getattr(value.cls, self.attr_name)

	def set_value(self, value, **locals):
		setattr(self.inst.eval(**locals), self.attr_name, value)

	def eval(self, **locals):
		return self.get_value(**locals).eval(**locals)

