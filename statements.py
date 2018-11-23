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
		return [s.exec() for s in statements][-1]

class Assignment(Statement):
	def __init__(self, var, value):
		self.var = var
		self.value = value

	def exec(self):
		if type(self.var) is Variable:
			self.var.value = self.value
			return
		else:
			self.var = self.value.eval()
			return

	def __str__(self):
		return f"{str(self.var)} := {self.value}"