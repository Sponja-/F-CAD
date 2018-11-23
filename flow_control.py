from elements import *

class Conditional(Operation):
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