from elements import *

class Conditional(Operation):
	def __init__(self, conditions, results, default=None):
		self.conditions = conditions
		self.results = results
		self.default = default

	def eval(self):
		for condition, result in zip(self.conditions, self.results):
			if condition.eval():
				return action.eval()
		if self.default is not None:
			return self.default.eval()
	
	def __str__(self):
		return '\n' + \
			   '\n'.join(f"| {str(condition)} ? {str(result)}" for condition, result in zip(self.conditions, self.results)) + \
			   (f"\n| {str(self.default)}" if self.default is not None else '\n')