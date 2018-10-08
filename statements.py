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
			return self.var.value
		else:
			self.var = self.value.eval()
			return self.var

	def __str__(self):
		return f"{str(self.var)} := {self.value}"

class IfElse(Statement):
	def __init__(self, condition, true_statement, false_statement):
		self.condition = condition
		self.true_statement = true_statement
		self.false_statement = false_statement

	def exec(self):
		return true_statement.exec() if condition.eval() else false_statement.exec()

class For(Statement):
	def __init__(self, symbol, iterable, statement):
		self.symbol = symbol
		self.iterable = iterable
		self.statement = statement

	def exec(self):
		for elem in self.iterable.eval():
			val = elem if type(elem) is Variable else classes_for_values[type(elem)](elem)
			with temp_vars(**{self.symbol: val}):
				result = self.statment.exec()
		return result

class While(Statement):
	def __init__(self, condition, statement):
		self.condition = condition
		self.statement = 

	def exec(self):
		while self.condition.eval():
			result = self.statement.exec()
		return result