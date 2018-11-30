from elements import Variable
from simplify import classes_for_values

class Statement:
	def exec(self):
		pass

	def eval(self):
		return self.exec()

class StatementList(Statement):
	def __init__(self, statements):
		self.statements = statements

	def exec(self):
		return [s.eval() for s in self.statements][-1]

	def __str__(self):
		return '\n'.join(str(s) for s in self.statements)

class Assignment(Statement):
	def __init__(self, var, value):
		self.var = var
		self.value = value

	def exec(self):
		self.var.value = self.value

	def __str__(self):
		return f"{str(self.var)} := {self.value}"

class AbsoluteAssignment(Statement):
	def __init__(self, var, value):
		self.var = var
		self.value = value

	def exec(self):
		val = self.value.eval()
		self.var.value = classes_for_values[type(val)](val)