from tokenizer import *
from elements import *
from arithmetic import *
from algebra import *
from trigonometry import *
from logic import *
from set_theory import *
from simplify import *
from calculus import *
from statements import *
from flow_control import *
from special_functions import *
from iterable import *
from argparse import ArgumentParser

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
	'-': Substraction,
	':': AppendTo
}

comparative_operators = {
	'<': Lesser,
	'<=': LesserOrEqual,
	'>': Greater,
	'>=': GreaterOrEqual,
	'==': Equal,
	'!=': NotEqual,
	'in': Contains
}

logic_operators = {
	'and': Conjunction,
	'or': InclusiveDisjunction,
	'xor': ExclusiveDisjunction
}

unary_operators = {
	'not': Negation
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
	'all': All,
	'diff': Differentiate,
	'print': Print,
	'graph': Graph,
	'scatter': Scatter,
	'show': Show,
	'take': Take,
	'tail': Tail
}

closing = {
	'[': ']',
	'(': ')',
	'{': '}'
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

	@property
	def next_token(self):
		if self.pos < len(self.tokens) - 1:
			return self.tokens[self.pos + 1]
		self.pos -= 2
		self.error()
	
	def error(self, message=""):
		print(f"Error on {self.token} at pos {self.pos}:\n\t{message}")
		raise SyntaxError

	def eat(self, token_type, value=None):
		if self.token.type != token_type or (value and self.token.value != value):
			self.error(f"Expected {names[token_type]}" + f" of value {value}" if value is not None else "")
		else:
			self.pos += 1

	def find_next(self, type):
		for i, token in enumerate(self.tokens[self.pos:]):
			if token.type == type:
				return self.pos + i
		return -1

	def find_closing(self):
		value = self.token.value
		assert(value in closing)
		open_chars = 1
		for i, token in enumerate(self.tokens[self.pos + 1:]):
			if token.value == value:
				open_chars += 1
			elif token.value == closing[value]:
				open_chars -= 1
			if open_chars == 0:
				return self.pos + i + 1
		self.error(f"Couldn't find closing '{value}'")

	def statement(self):
		types = [token.type for token in self.tokens[self.pos:self.find_next(SEMICOLON)]]

		if ASSIGNMENT in types:
			return self.assignment_statement()

		return self.eval_statement()

	def statement_list(self):
		s = self.statement()
		result = [s] if s is not None else []
		while self.token.type == SEMICOLON:
			self.eat(SEMICOLON)
			s = self.statement()
			if s is not None:
				result.append(s)
		return StatementList(result)

	def assignment_statement(self):
		result = self.token
		self.eat(NAME)
		
		if self.token.type == GROUP_CHAR:
			arguments = [arg.symbol for arg in self.tuple_list()]
			self.eat(ASSIGNMENT)
			return Assignment(Variable(result.value), Function(arguments, self.expr()))
		
		self.eat(ASSIGNMENT)
		return Assignment(Variable(result.value), self.expr())

	def eval_statement(self):
		return self.expr()

	def tuple_list(self):
		self.eat(GROUP_CHAR, '(')
		result = [self.expr()]

		while self.token.type == COMMA:
			self.eat(COMMA)
			result.append(self.expr())

		self.eat(GROUP_CHAR, ')')
		return result

	def subscript_index(self): # Not implemented
		self.eat(GROUP_CHAR, '[')
		result = [self.expr()]

		while self.token.type == COMMA:
			self.eat(COMMA)
			result.append(self.expr())

		self.eat(GROUP_CHAR, ']')
		return Vector(*result)

	def vector_constant(self):
		self.eat(GROUP_CHAR, '[')
		result = [self.expr()]

		while self.token.type == COMMA:
			self.eat(COMMA)
			result.append(self.expr())

		self.eat(GROUP_CHAR, ']')
		return result

	def range_expr(self):
		self.eat(GROUP_CHAR, '[')
		start = self.expr()
		second = None
		end = None

		if self.token.type == COMMA:
			self.eat(COMMA)
			second = self.expr()

		self.eat(RANGE)

		if self.token.value != ']':
			end = self.expr()

		self.eat(GROUP_CHAR, ']')
		return Range(start, end, second)

	def list_comp_expr(self):
		self.eat(GROUP_CHAR, '[')
		term = self.expr()
		self.eat(KEYWORD, "for")
		term_symbol = self.token.value
		self.eat(NAME)
		self.eat(KEYWORD, "in")
		list = self.expr()
		conditions = one
		if self.token.type == CONDITION:
			self.eat(CONDITION)
			conditions = self.expr()
		self.eat(GROUP_CHAR, ']')
		return ListComprehension(term_symbol, term, conditions, list)

	def bracket_expr(self):
		if self.next_token.value == ']':
			self.eat(GROUP_CHAR, '[')
			self.eat(GROUP_CHAR, ']')
			return Vector()
		tokens = [(token.type, token.value) for token in self.tokens[self.pos:self.find_closing()]]
		types, values = [[token[i] for token in tokens] for i in (0, 1)]
		if 'for' in values:
			return self.list_comp_expr()
		if RANGE in types:
			return self.range_expr()
		return Vector(*self.vector_constant())

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
				return FunctionCall(Variable(token.value), *arguments)

			if self.token.value == '[':
				self.eat(GROUP_CHAR)
				index = self.expr()
				self.eat(GROUP_CHAR, ']')
				return Subscript(Variable(token.value), index)

			return Variable(token.value)

		if token.type == GROUP_CHAR:
			if token.value == '(':
				self.eat(GROUP_CHAR)
				token = self.expr()
				self.eat(GROUP_CHAR, ')')
				return token

			if token.value == '[':
				return self.bracket_expr()

	def binary_operator_list(self, operators, operand_function):
		result = operand_function()

		while self.token.value in operators.keys():
			token = self.token
			if self.token.value == 'in':
				self.eat(KEYWORD)
			else:
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

	def unary_expr(self):
		if self.token.value in unary_operators.keys():
			token = self.token
			self.eat(OPERATOR)
			return unary_operators[token.value](self.expr())

		return self.logic_expr()

	def conditional_list_expr(self):
		if self.token.type == CONDITION:
			conditions = []
			results = []
			default = None
			while self.token.type == CONDITION:
				self.eat(CONDITION)
				conditions.append(self.expr())
				if self.token.type == QUESTION:
					self.eat(QUESTION)
					results.append(self.expr())
					if self.token.type == SEMICOLON and self.next_token.type == CONDITION:
						self.eat(SEMICOLON)
				else:
					default = conditions.pop()
					break
			return Conditional(conditions, results, default)
					
		return self.unary_expr()


	def expr(self):
		return self.conditional_list_expr()

debug = False

if __name__ == '__main__':
	parser = ArgumentParser(description="Interprets a file, or works as a REPL if none is provided")
	parser.add_argument('file', type=str, help='File to interpret', nargs='?')

	args = parser.parse_args()

	if args.file is not None:
		with open(args.file, 'r') as file:
			Parser(Tokenizer(file.read().strip())).statement_list().eval()
	else:
		while True:
			result = Parser(Tokenizer(input('> '))).statement_list()
			if debug:
				print(str(result))
			else:
				value = result.eval() 
				if value is not None:
					print(value)