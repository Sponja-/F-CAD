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
			   (f"\n| {str(self.default)}" if self.default is not None else '\n')

class ForLoop:
	def __init__(self, symbols, range, operation):
		self.symbols = symbols
		self.range = range
		self.operation = operation

	def eval(self, **locals):
		new_locals = locals.copy()
		for value in self.range.eval(**locals):
			if len(self.symbols) <= 1:
				new_locals[self.symbols[0]] = classes_for_values[type(value)](value)
			else:
				for symbol, val in zip(self.symbols, value):
					new_locals[symbol] = classes_for_values[type(value)](value)
			self.operation.eval(**new_locals)

class WhileLoop:
	def __init__(self, condition, operation):
		self.condition = condition
		self.operation = operation

	def eval(self, **locals):
		while self.condition.eval(**locals):
			self.operation.eval(**locals)