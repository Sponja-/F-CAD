#
# I/O
#

print = print
input = input

import json
encode = json.dumps
decode = json.loads

def read(file_path):
	with open(file_path, 'r') as file:
		return file.read()

def write(file_path, contents):
	with open(file_path, 'w') as file:
		file.write(contents)

def graph(free, bound):
	plt.plot(free, bound)
	plt.show()

def scatter(xs, ys):
	plt.scatter(xs, ys)
	plt.show()

#
# MATH
#

import itertools

cartesian_product = lambda x, y: list(itertools.product(x, y))
combinations = lambda x, y: list(itertools.combinations(x, int(y)))
permutations = lambda x, y: list(itertools.permutations(x, int(y)))

from numpy import sin, cos, tan, arcsin, arccos, arctan, floor, ceil, trunc, abs, degrees, radians, arctan2, sum, log10, log2, sqrt, cbrt, pi, e, dot
import numpy as np

round = np.round_
product = np.prod
ln = np.log
infinity = np.inf
negative_infinity = -np.inf
log = lambda x, y: np.log(x) / np.log(y)
any = lambda x: x.any()
all = lambda x: x.all()
shape = lambda x: x.shape
number = lambda x: float(x)

#
# LIST
#

len = len
take = lambda x, y=1: np.array(list(itertools.islice(x, int(y))))

def __tail__(arr, amount):
	iterable = iter(arr)
	index = 0
	for x in iterable:
		if index >= amount:
			yield x
			break
		index += 1
	for x in iterable:
		yield x

tail = lambda x, y=1: np.array(list(__tail__(x, int(y))))
slice = lambda x, y, z, w=1: np.array(list(itertools.islice(x, int(y), int(z), int(w))))
reverse = lambda x: np.array(list(reversed(x)))
max = max
min = min

#
# STRING
#

ord = ord

def char(x):
	return chr(int(x))