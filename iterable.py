from elements import Constant, Operation, FunctionCall, classes_for_values
from constants import one
from arithmetic import Addition
from numpy import array, arange, sum, append
from itertools import count, islice

class Len(Operation):
	def __init__(self, arr):
		operation = len
		super().__init__(operation, arr)

class Range(Operation):
	def __init__(self, start, end=None, second=None):
		if second is None:
			second = Addition(start, one)
		if end is not None:
			operation = lambda x, y, z: arange(x, y, z - x)
		else:
			end = one
			operation = lambda x, y, z: count(x, z - x)
		super().__init__(operation, start, end, second)

	def __str__(self):
		return f"({str(self.operands[0])}, {str(self.operands[0] + self.operands[2])} ... {str(self.operands[1])})"

class AppendTo(Operation):
	def __init__(self, vec, appended):
		operation = append
		super().__init__(operation, vec, appended)

class ListComprehension(Operation):
	def __init__(self, term_symbol, term, conditions, list):
		def operation(term_symbol, term, conditions, list, locals):
			result = []
			new_locals = locals.copy()
			for x in list:
				new_locals[term_symbol] = classes_for_values[type(x)](x)
				if conditions.eval(**new_locals):
					result.append(term.eval(**new_locals))
			return array(result)
		super().__init__(operation, term_symbol, term, conditions, list)

	def eval(self, **locals):
		return self.operation(*self.operands[:3], self.operands[3].eval(**locals), locals)


class Take(Operation):
	def __init__(self, arr, amount=one):
		operation = lambda x, y: array(list(islice(x, int(y))))
		super().__init__(operation, arr, amount)

def tail(arr, amount):
	iterable = iter(arr)
	index = 0
	for x in iterable:
		if index >= amount:
			yield x
			break
		index += 1
	for x in iterable:
		yield x

class Tail(Operation):
	def __init__(self, arr, amount=one):
		operation = lambda x, y: array(list(tail(x, int(y))))
		super().__init__(operation, arr, amount)

class Slice(Operation):
	def __init__(self, arr, start, end, step=one):
		operation = lambda x, y, z, w: array(list(islice(x, int(y), int(z), int(w))))
		super().__init__(operation, arr, start, end, step)

class SumElements(Operation):
	def __init__(self, terms):
		operation = sum
		super().__init__(operation, terms, symbol="sum")
