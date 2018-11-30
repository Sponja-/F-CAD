from elements import Variable
from simplify import classes_for_values

class Statement:
	def exec(self, **locals):
		pass

	def eval(self, **locals):
		return self.exec(**locals)

class StatementList(Statement):
	def __init__(self, statements):
		self.statements = statements

	def exec(self):
		return [s.eval() for s in self.statements][-1]

	def __getitem__(self, index):
		return self.statements[index]

	def __str__(self):
		return '\n'.join(str(s) for s in self.statements)

class Assignment(Statement):
	def __init__(self, var, value):
		self.var = var
		self.value = value

	def exec(self):
		self.var.value = self.value
		return self.value

	def __str__(self):
		return f"{str(self.var)} := {self.value}"

class AbsoluteAssignment(Statement):
	def __init__(self, var, value):
		self.var = var
		self.value = value

	def exec(self, **locals):
		val = self.value.eval(**locals)
		self.var.value = classes_for_values[type(val)](val)
		return val