from elements import Variable, classes_for_values, ret_val

class Statement:
	def exec(self, **locals):
		pass

	def eval(self, **locals):
		return self.exec(**locals)

class Return:
	def __init__(self, operation):
		self.operation = operation

	def eval(self, **locals):
		return ret_val(self.operation.eval(**locals))

class StatementList(Statement):
	def __init__(self, statements):
		self.statements = statements

	def exec(self, **locals):
		for statement in self.statements:
			value = statement.eval(**locals)
			if type(value) is ret_val:
				return value

	def __getitem__(self, index):
		return self.statements[index]

	def __str__(self):
		return '\n'.join(str(s) for s in self.statements)

class ScopedStatements(StatementList):
	def __init__(self, statements):
		self.statements = statements

	def exec(self, **locals):
		old = Variable.table.copy()
		ret_val = super().exec(**locals)
		Variable.table = old
		return ret_val

class Assignment(Statement):
	def __init__(self, var, value):
		self.var = var
		self.value = value

	def exec(self, **locals):
		if self.var.symbol in locals:
			locals[var.symbol] = self.value
		else:
			self.var.value = self.value

	def __str__(self):
		return f"{str(self.var)} := {self.value}"

class AbsoluteAssignment(Assignment):
	def __init__(self, var, value):
		super().__init__(var, value)

	def exec(self, **locals):
		val = self.value.eval(**locals)
		self.value = classes_for_values[type(val)](val)
		super().exec(**locals)
		return self.value.eval(**locals)