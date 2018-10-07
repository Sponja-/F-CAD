from elements import Variable

class Statement:
	def eval(self):
		return self.exec()

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

