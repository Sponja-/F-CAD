from tokenizer import *
from elements import *
from arithmetic import *
from algebra import *
from trigonometry import *
from logic import *
from set_theory import *
from simplify import *
from calculus import *

power_operators = {
	'^': Exponentiation,
	'row': Row,
	'col': Column,
	'P': Permutations,
	'C': Combinations
}

factor_operators = {
	'.': DotProduct,
	'*': Multiplication,
	'/': Division,
	'%': Modulo
}

term_operators = {
	'+': Addition,
	'-': Substraction
}

comparative_operators = {
	'<': Lesser,
	'<=': LesserOrEqual,
	'>': Greater,
	'>=': GreaterOrEqual,
	'=': Equal,
	'!=': NotEqual,
	'in': Contains
}

logic_operators = {
	'and': Conjunction,
	'or': InclusiveDisjunction,
	'xor': ExclusiveDisjunction
}

argument_list_operators = {
	'sqrt': SquareRoot,
	'root': NthRoot,
	'log': Logarithm,
	'ln': LogarithmBaseE,
	'lg': LogarithmBase2,
	'inv': Inverse,
	'abs': AbsoluteValue,
	'sin': Sine,
	'cos': Cosine,
	'tan': Tangent,
	'arcsin': ArcSine,
	'arccos': ArcCosine,
	'arctan': ArcTangent,
	'any': Any,
	'all': All
}

class Parser:
	def __init__(self, tok_gen):
		self.tokens = list(tok_gen.tokens())
		self.pos = 0

	@property
	def token(self):
		if self.pos < len(self.tokens):
			return self.tokens[self.pos]
		self.pos -= 1
		self.error()

	def error(self):
		print(f"Error on {self.token} at pos {self.pos}")
		raise SyntaxError

	def eat(self, token_type, value=None):
		if self.token.type != token_type or (value and self.token.value != value):
			self.error()
		else:
			self.pos += 1

	def assignment(self):
		result = self.token
		self.eat(NAME)
		
		if self.token.type == 'GROUP':
			arguments = [arg.symbol for arg in self.tuple_list()]
			return Assignment(Variable(result.value), Function(arguments, self.expr()))
		
		self.eat(OPERATOR, ':=')
		return Assignment(Variable(result.value), self.expr())

	def eval_statement(self):
		return self.expr()

	def tuple_list(self):
		self.eat(GROUP, '(')
		result = [self.expr()]
		while self.token.type == COMMA:
			self.eat(COMMA)
			result.append(self.expr())
		self.eat(GROUP, ')')
		return result

	def subscript_index(self):
		self.eat(GROUP, '[')
		result = [self.expr()]
		while self.token.type == COMMA:
			self.eat(COMMA)
			result.append(self.expr())
		self.eat(GROUP, ']')
		return Vector(result)

	def vector_constant_elem(self):
		if self.token.value == '[':
			return self.vector_constant()
		if self.token.type == NUMBER:
			result = token.value
			self.eat(NUMBER)
			return Number(result)
		self.error()

	def vector_constant(self):
		self.eat(GROUP, '[')
		result = [self.vector_constant_elem()]
		while self.token.type == COMMA:
			self.eat(COMMA)
			result.append(self.vector_constant_elem())
		self.eat(GROUP, ']')
		return result

	def atom(self):
		token = self.token

		if token.type == NUMBER:
			self.eat(NUMBER)
			return Number(token.value)

		if token.type == OPERATOR:
			self.eat(OPERATOR)

			if token.value == '-':
				return Inverse(self.expr())
			
			assert(token.value in argument_list_operators.keys())
			args = self.tuple_list()
			return argument_list_operators[token.value](*args)

		if token.type == NAME:
			self.eat(NAME)

			if self.token.value == '(':
				arguments = self.tuple_list()
				return FunctionCall(token.value, argument)

			if self.token.value == '[':
				index = self.subscript_index()
				self.eat(GROUP)
				return Subscript(token.value, index)

			return Variable(token.value)

		if token.type == GROUP:
			if token.value == '(':
				self.eat(GROUP)
				token = self.expr()
				self.eat(GROUP, ')')
				return token

			if token.value == '[':
				return Vector(self.vector_constant())

	def binary_operator_list(self, operators, operand_function):
		result = operand_function()

		while self.pos < len(self.tokens) and self.token.value in operators.keys():
			token = self.token
			self.eat(OPERATOR)
			result = operators[token.value](result, operand_function())

		return result

	def power(self):
		return self.binary_operator_list(power_operators, self.atom)

	def factor(self):
		return self.binary_operator_list(factor_operators, self.power)

	def term(self):
		return self.binary_operator_list(term_operators, self.factor)

	def comparation(self):
		return self.binary_operator_list(comparative_operators, self.term)

	def logic_expr(self):
		return self.binary_operator_list(logic_operators, self.comparation)

	def expr(self):
		if self.token.value == 'not':
			self.eat(OPERATOR)
			return Negation(self.expr())

		return self.logic_expr()

if __name__ == '__main__':
	while True:
		option = input("E/A/VARS?> ")
		
		if option == 'VARS':
			print('\n'.join([f'{symbol}: {str(value)}' for symbol, value in Variable.table.items()]))

		else:
			p = Parser(Tokenizer(input('> ')))
			if option == 'E':
				result = p.eval_statement()
			elif option == 'A':
				result = p.assignment()
			
			print(result.eval())