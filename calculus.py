from elements import Operation, Function, Variable
from arithmetic import *
from consants import *
from trigonometry import *

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

	Exponentiation: lambda f, g, df, dg:
		Multiplication(
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
		),

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

	NthRoot: NthRoot_derivative,

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

def Logarithm_derivative(f, g, df, dg):
	if type(g) is not Number:
		except NotImplementedError
	return Division(
		df,
		Multiplication(
				LogarithmBaseE(g),
				f
			)
		)

def NthRoot_derivative(f, g, df, dg):
	return operation_derivatives[Exponentiation](f, Inverse(g), df, operation_derivatives[Inverse](g, dg))

def differentiate(f, var_symbol):
	if type(f) is Function:
		assert(var_symbol in f.value.symbols)
		return differentiate(f.value.operation, var_symbol)
	elif isinstance(f, Operation):
		return operation_derivatives[type(f)](f.operands, *(differentiate(op) for op in f.operands))
	elif type(f) is Variable:
		if f.symbol == var_symbol:
			return one
		else:
			return f
	elif type(f) is Number:
		return zero

class Differentiate(Operation):
	def __init__(self, function, var_symbol):
		operation = differentiate
		super().__init__(operation, function, var_symbol)