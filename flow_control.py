from elements import *

class Conditional:
	def __init__(self, conditions, results, default=None):
		self.conditions = conditions
		self.results = results
		self.default = default

	def eval(self, **locals):
		for condition, result in zip(self.conditions, self.results):
			if condition.eval(**locals):
				return result.eval(**locals)
		if self.default is not None:
			return self.default.eval(**locals)

	def __str__(self):
		return '\n' + \
			   '\n'.join(f"| {str(condition)} ? {str(result)}" for condition, result in zip(self.conditions, self.results)) + \
			   (f"\n| otherwise {str(self.default)}" if self.default is not None else '\n')

class IfElseStatement:
	def __init__(self, condition, true_result, false_result = None):
		self.condition = condition
		self.true_result = true_result
		self.false_result = false_result

	def eval(self, **locals):
		if self.condition.eval(**locals):
			self.true_result.eval(**locals)
		elif self.false_result is not None:
			self.false_result.eval(**locals)

class ForLoop:
	def __init__(self, symbols, range, operation):
		self.symbols = symbols
		self.range = range
		self.operation = operation

	def eval(self, **locals):
		new_locals = locals.copy()
		for value in self.range.eval(**locals):
			if len(self.symbols) <= 1:
				new_locals[self.symbols[0]] = convert_type(value)
			else:
				for symbol, val in zip(self.symbols, value):
					new_locals[symbol] = convert_type(value)
			self.operation.eval(**new_locals)

class WhileLoop:
	def __init__(self, condition, operation):
		self.condition = condition
		self.operation = operation

	def eval(self, **locals):
		while self.condition.eval(**locals):
			self.operation.eval(**locals)