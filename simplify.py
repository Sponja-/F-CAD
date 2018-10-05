from elements import Number, Operation
from arithmetic import *
from constants import zero, one
from set_theory import Set
from algebra import Vector
from numpy import array

def s_Addition(op):
	if type(op.operands[0]) is Number:
		op.operands[0], op.operands[1] = op.operands[1], op.operands[0]
	if type(op.operands[1]) is Number and op.operands[1].value == 0:
		return op.operands[0]
	return op

s_Substraction = s_Addition

def s_Multiplication(op):
	if type(op.operands[0]) is Number:
		op.operands[0], op.operands[1] = op.operands[1], op.operands[0]
	if type(op.operands[1]) is Number:
		if op.operands[1].value == 0:
			return op.operands[1]
		if op.operands[1].value == 1:
			return op.operands[0]
	return op

def s_Division(op):
	if type(op.operands[0]) is Number:
		op.operands[0], op.operands[1] = op.operands[1], op.operands[0]
	if type(op.operands[1]) is Number:
		if op.operands[1].value == 0:
			except ZeroDivisionError
		if op.operands[1].value == 1:
			return op.operands[0]
	return op

def s_Exponentiation(op):
	if type(op.operands[0]) is Number:
		if op.operands[0].value == 0 or op.operands[0].value == 1:
			return op.operands[0].value
	if type(op.operands[1]) is Number:
		if op.operands[1].value == 0:
			return one
		if op.operands[1].value == 1:
			return op.operands[0]
	return op

def s_SquareRoot(op):
	if type(op.operands[0]) is Number and op.operands[0].value == 1:
		return op.operands[0].value
	return op

def s_NthRoot(op):
	if type(op.operands[1]) is Number and op.operands[1].value == 1:
		return op.operands[1].value
	return op

def s_Logarithm(op):
	if type(op.operands[0]) is Number:
		if op.operands[0].value <= 0:
			except ValueError
		if op.operands[0].value == 1:
			return zero
	return op

s_CommonLogarithm = s_Logarithm
s_LogarithmBase2 = s_Logarithm
s_LogarithmBaseE = s_Logarithm

operation_simplifications = {
	Addition: s_Addition,
	Substraction: s_Substraction,
	Multiplication: s_Multiplication,
	Division: s_Division,
	Exponentiation: s_Exponentiation,
	SquareRoot: s_SquareRoot,
	NthRoot: s_NthRoot,
	Logarithm: s_Logarithm,
	CommonLogarithm: s_CommonLogarithm,
	LogarithmBase2: s_LogarithmBase2,
	LogarithmBaseE: s_LogarithmBaseE
}

classes_for_values = {
	set: Set,
	int: Number,
	float: Number,
	list: Vector,
	array: Vector
}

def simplify(op):
	if type(op) is Operation:
		if all([type(x) == Constant for x in op.operands]):
			result = op.operation(*[x.value for x in op.operands])
			return classes_for_values[type(result)](result)
		return operation_simplifications.get(type(op), op)
	return op