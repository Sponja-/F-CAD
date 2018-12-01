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
	'in': Contains,
	'union': Union,
	'intersection': Intersection
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
	'tail': Tail,
	'len': Len,
	'slice': Slice,
	'input': Input
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
			self.error(f"Expected {names[token_type]}" + (f" of value {value}" if value is not None else ""))
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

	def statement_list(self):
		s = self.expr()
		result = [s] if s is not None else []
		while self.token.value != '}' and self.token.type != EOF:
			self.eat(SEMICOLON)
			s = self.expr()
			if s is not None:
				result.append(s)
		return StatementList(result)

	def expr_list(self):
		if self.token.value in closing.values():
			return []
		result = [self.expr()]

		while self.token.type == COMMA:
			self.eat(COMMA)
			result.append(self.expr())

		return result

	def tuple_list(self):
		self.eat(GROUP_CHAR, '(')
		result = self.expr_list()
		self.eat(GROUP_CHAR, ')')
		return result

	def vector_constant(self):
		self.eat(GROUP_CHAR, '[')
		result = self.expr_list()
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
		if self.token.type == SEPARATOR:
			self.eat(SEPARATOR)
			conditions = self.expr()
		self.eat(GROUP_CHAR, ']')
		return ListComprehension(term_symbol, term, conditions, list)

	def bracket_expr(self):
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
			return Variable(token.value)

		if token.type == GROUP_CHAR:
			if token.value == '(':
				self.eat(GROUP_CHAR)
				token = self.expr()
				self.eat(GROUP_CHAR, ')')
				return token

			if token.value == '[':
				return self.bracket_expr()

			if token.value == '{':
				self.eat(GROUP_CHAR)
				result = self.expr_list()
				self.eat(GROUP_CHAR, '}')
				return Set(*result)


	def trailer_expr(self):
		result = self.atom()
		while self.token.value in closing.keys():
			if self.token.value == '(':
				arguments = self.tuple_list()
				result = FunctionCall(result, *arguments)
			elif self.token.value == '[':
				self.eat(GROUP_CHAR)
				indeces = self.expr_list()
				self.eat(GROUP_CHAR)
				result = Subscript(result, *indeces)
		return result

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
		return self.binary_operator_list(power_operators, self.trailer_expr)

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
		if self.token.type == SEPARATOR:
			conditions = []
			results = []
			default = None
			while self.token.type == SEPARATOR:
				self.eat(SEPARATOR)
				if self.token.value == "otherwise":
					self.eat(KEYWORD)
					default = self.unary_expr()
					break
				else:
					conditions.append(self.unary_expr())
					self.eat(QUESTION)
					results.append(self.unary_expr())
			return Conditional(conditions, results, default)
		return self.unary_expr()

	def where_expr(self):
		result = self.conditional_list_expr()
		if self.token.value == "where":
			self.eat(KEYWORD)
			if self.token.type == SEPARATOR:
				assignments = {}
				while self.token.type == SEPARATOR:
					self.eat(SEPARATOR)
					assignment = self.assignment_expr(absolute_assignment=False)
					assignments[assignment.var.symbol] = assignment.value
			else:
				assignment = self.assignment_expr(absolute_assignment=False)
				assignments = {assignment.var.symbol: assignment.value}
			return Where(result, assignments)
		return result

	def assignment_expr(self, **kwargs):
		a = AbsoluteAssignment if kwargs.get("absolute_assignment", absolute_assignment_default) else Assignment
		start_pos = self.pos

		if self.token.type != NAME:
			return self.where_expr()

		result = self.token
		self.eat(NAME)
		
		if self.token.value == '(':
			try:
				arguments = [arg.symbol for arg in self.tuple_list()]
			except AttributeError:
				self.pos = start_pos
				return self.where_expr()
			if self.token.type == ASSIGNMENT:
				self.eat(ASSIGNMENT)
				return a(Variable(result.value), Function(arguments, self.statement_block()))
		
		if self.token.type == ASSIGNMENT:
			self.eat(ASSIGNMENT)
			return a(Variable(result.value), self.expr())
		else:
			self.pos = start_pos
			return self.where_expr()

	def return_expr(self):
		if self.token.value == 'return':
			self.eat(KEYWORD)
			return Return(self.assignment_expr())
		return self.assignment_expr()

	def expr(self):
		return self.return_expr()

	def statement_block(self):
		if self.token.value != '{':
			return self.expr()
		self.eat(GROUP_CHAR)
		result = self.statement_list()
		self.eat(GROUP_CHAR, '}')
		return result


debug = False
absolute_assignment_default = True

if __name__ == '__main__':
	parser = ArgumentParser(description="Interprets a file, or works as a REPL if none is provided")
	parser.add_argument('file', type=str, help='File to interpret', nargs='?')

	args = parser.parse_args()

	if args.file is not None:
		with open(args.file, 'r') as file:
			Parser(Tokenizer(file.read().strip())).statement_list().eval()
	else:
		while True:
			result = Parser(Tokenizer(input('> '))).expr()
			if debug:
				print(str(result))
			else:
				value = result.eval() 
				if not isinstance(result, Statement):
					print(value)