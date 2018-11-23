from elements import Operation, Function, Variable
from arithmetic import *
from constants import *
from trigonometry import *
from numpy import log

def Logarithm_derivative(f, g, df, dg):
	if type(g) is not Number:
		raise NotImplementedError
	return Division(
		df,
		Multiplication(
				LogarithmBaseE(g),
				f
			)
		)

def Exponentiation_derivative(f, g, df, dg):
	if type(f) is Number:
		return Multiplication(
				Multiplication(
					Number(log(f.value)),
					Exponentiation(f, g)
				),
				dg
			)
	if type(g) is Number:
		return Multiplication(
				Multiplication(
					g,
					Exponentiation(f, Number(g.value - 1))
				),
				df
			)
	return Multiplication(
			Exponentiation(
				e,
				Multiplication(
					g,
					LogarithmBaseE(f)
					)
				),
			Addition(
				Multiplication(
					dg,
					LogarithmBaseE(f)
				),
				Multiplication(
					Division(g, f),
					df
				)
			)
		)

operation_derivatives = { 
	Addition: lambda f, g, df, dg:
		Addition(df, dg),

	Substraction: lambda f, g, df, dg:
		Substraction(df, dg),

	Multiplication: lambda f, g, df, dg:
		Addition(
			Multiplication(df, g),
			Multiplication(f, dg)
		),

	Division: lambda f, g, df, dg:
		Division(
			Substraction(
				Multiplication(df, g),
				Multiplication(f, dg)
			),
			Exponentiation(g, 2)
		),

	Exponentiation:	Exponentiation_derivative,

	SquareRoot: lambda f, df:
		Multiplication(
			df,
			Inverse(
				Multiplication(
					two,
					SquareRoot(f)
				)
			)
		),

	NthRoot: None,

	Logarithm: Logarithm_derivative,

	CommonLogarithm: Logarithm_derivative,

	LogarithmBase2: Logarithm_derivative,

	LogarithmBaseE: lambda f, g, df, dg:
		Multiplication(
			df,
			Inverse(f),
		),

	Opposite: lambda f, df:
		Opposite(df),

	Inverse: lambda f, df:
		Opposite(
			Multiplication(
				df,
				Inverse(
					Exponentiation(f, 2)
				)
			)
		),

	Sine: lambda f, df:
		Multiplication(
			Cosine(f),
			df
		),

	Cosine: lambda f, df:
		Opposite(
			Multiplication(
				Sine(f),
				df
			)
		),

	Tangent: lambda f, df:
		Division(
			df,
			Exponentiation(
				Cosine(f),
				2
			)
		),

	ArcSine: lambda f, df:
		Division(
			df,
			SquareRoot(
				Substraction(
					one,
					Exponentiation(f, 2)
				)
			)
		),

	ArcCosine: lambda f, df:
		Opposite(
			Division(
			df,
			SquareRoot(
				Substraction(
					one,
					Exponentiation(f, 2)
					)
				)
			)
		),

	ArcTangent: lambda f, df:
		Division(
			df,
			Addition(
				one,
				Exponentiation(f, 2)
			)
		)
}

operation_derivatives[NthRoot] = lambda f, g, df, dg: operation_derivatives[Exponentiation](f, Inverse(g), df, operation_derivatives[Inverse](g, dg))

def derivative(f, var_symbol):
	if type(f) is Function:
		if var_symbol in f.value.symbols:
			return derivative(f.value.operation, var_symbol)
		return zero
	elif isinstance(f, Operation):
		return operation_derivatives[type(f)](*f.operands, *(derivative(op, var_symbol) for op in f.operands))
	elif type(f) is Variable:
		if f.symbol == var_symbol:
			return one
		else:
			return f
	elif type(f) is Number:
		return zero
	return f

class Differentiate(Operation):
	def __init__(self, function, var):
		operation = derivative
		super().__init__(operation, function, var)

	def eval(self, **locals):
		return self.operation(self.operands[0] if type(self.operands[0]) is not Variable else self.operands[0].value, self.operands[1].symbol)

	def __str__(self):
		return f"d({str(self.operands[0])})/d{self.opernads[1]}"