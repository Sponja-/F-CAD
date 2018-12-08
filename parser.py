from tokenizer import *
from elements import *
from arithmetic import *
from algebra import *
from trigonometry import *
from logic import *
from set_theory import *
from statements import *
from flow_control import *
from special_functions import *
from iterable import *
from strings import *
from argparse import ArgumentParser

class Import(Operation):
	def __init__(self, file_path):
		def operation(x):
			with open(x, 'r') as source_file:
				parse_string(source_file.read())
		super().__init__(operation, file_path)

power_operators = {
	'^': Exponentiation,
	'row': Row,
	'col': Column,
	'P': Permutations,
	'C': Combinations
}

factor_operators = {
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
	'print': Print,
	'graph': Graph,
	'scatter': Scatter,
	'show': Show,
	'take': Take,
	'tail': Tail,
	'len': Len,
	'slice': Slice,
	'input': Input,
	'shape': Shape,
	'floor': Floor,
	'ceil': Ceil,
	'trunc': Truncate,
	'ord': CharToCode,
	'chr': CodeToChar,
	'number': ToNumber,
	'read': Read,
	'write': Write,
	'encode': JsonEncode,
	'decode': JsonDecode,
	'import': Import,
	'import_python': ImportPythonModule,
	'run_python': RunPython
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
		self.show_errors = True

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
		if self.show_errors:
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

	def expr_list(self):
		if self.token.value in closing.values():
			return []
		result = [self.expr()]

		while self.token.type == COMMA:
			self.eat(COMMA)
			result.append(self.expr())

		return result

	def name_list(self):
		if self.token.type != NAME:
			return []

		result = [self.token.value]
		self.eat(NAME)

		while self.token.type == COMMA:
			self.eat(COMMA)
			result.append(self.token.value)
			self.eat(NAME)

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
			assert(token.value in argument_list_operators.keys())
			args = self.tuple_list()
			return argument_list_operators[token.value](*args)

		if token.type == NAME:
			self.eat(NAME)
			return Variable(token.value)

		if token.type == STRING:
			self.eat(STRING)
			return String(token.value)

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

	def negative_expr(self):
		if self.token.value == '-':
			self.eat(OPERATOR)
			return Opposite(self.power())
		return self.power()

	def factor(self):
		return self.binary_operator_list(factor_operators, self.negative_expr)

	def term(self):
		return self.binary_operator_list(term_operators, self.factor)

	def comparation(self):
		return self.binary_operator_list(comparative_operators, self.term)

	def logic_expr(self):
		return self.binary_operator_list(logic_operators, self.comparation)

	def not_expr(self):
		if self.token.value == "not":
			self.eat(OPERATOR)
			return Negation(self.expr())

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
					default = self.not_expr()
					break
				else:
					conditions.append(self.not_expr())
					self.eat(QUESTION)
					results.append(self.not_expr())
			return Conditional(conditions, results, default)
		return self.not_expr()

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
		assign = AbsoluteAssignment if kwargs.get("absolute_assignment", absolute_assignment_default) else Assignment
		start_pos = self.pos

		if self.token.type != NAME:
			return self.where_expr()
		
		if self.next_token.value == '(':
			symbol = self.token
			self.eat(NAME)
			self.eat(GROUP_CHAR, '(')
			
			try:
				self.show_errors = False
				arguments = self.name_list()
				self.show_errors = True
			except:
				self.pos = start_pos
				return self.where_expr()
			
			if self.token.value == ')' and self.next_token.type == ASSIGNMENT:
				self.eat(GROUP_CHAR, ')')
				self.eat(ASSIGNMENT)
				return assign(Variable(symbol.value), Function(arguments, self.statement_block(scoped = True)))
			else:
				self.pos = start_pos
				return self.where_expr()

		
		try:
			self.show_errors = False
			symbols = self.name_list()
			self.show_errors = True
		except:
			self.pos = start_pos
			return self.where_expr()

		if self.token.type == ASSIGNMENT:
			self.eat(ASSIGNMENT)
			result = []
			exprs = self.expr_list()
			assert(len(symbols) == len(exprs))
			for symbol, expr in zip(symbols, exprs):
				result.append(assign(Variable(symbol), expr))
			if len(result) == 1:
				return result[0]
			return StatementList(result)
		else:
			self.pos = start_pos
			return self.where_expr()

	def expr(self):
		return self.assignment_expr()

	def return_statement(self):
		if self.token.value == 'return':
			self.eat(KEYWORD)
			return Return(self.expr())
		return self.expr()

	def for_statement(self):
		if self.token.value == 'for':
			self.eat(KEYWORD)
			self.eat(GROUP_CHAR, '(')
			symbols = self.name_list()
			self.eat(KEYWORD, 'in')
			range = self.expr()
			self.eat(GROUP_CHAR, ')')
			operation = self.statement_block()
			return ForLoop(symbols, range, operation)
		return self.return_statement()

	def while_statement(self):
		if self.token.value == 'while':
			self.eat(KEYWORD)
			self.eat(GROUP_CHAR, '(')
			condition = self.expr()
			self.eat(GROUP_CHAR, ')')
			operation = self.statement_block()
			return WhileLoop(condition, operation)
		return self.for_statement()

	def statement(self):
		return self.while_statement()

	def statement_list(self, **kwargs):
		s = self.statement()
		result = [s] if s is not None else []
		while self.token.value != '}' and self.token.type != EOF:
			self.eat(SEMICOLON)
			s = self.statement()
			if s is not None:
				result.append(s)
		return ScopedStatements(result) if kwargs.get("scoped", False) else StatementList(result)

	def statement_block(self, **kwargs):
		if self.token.value != '{':
			return self.statement()
		self.eat(GROUP_CHAR)
		result = self.statement_list()
		self.eat(GROUP_CHAR, '}')
		return result

def parse_string(s):
	Parser(Tokenizer(s.strip())).statement_list().eval()

debug = False
absolute_assignment_default = True

if __name__ == '__main__':
	parser = ArgumentParser(description="Interprets a file, or works as a REPL if none is provided")
	parser.add_argument('file', type=str, help='File to interpret', nargs='?')

	args = parser.parse_args()

	if args.file is not None:
		with open(args.file, 'r') as file:
			parse_string(file.read())
	else:
		while True:
			result = Parser(Tokenizer(input('> '))).expr()
			if debug:
				print(str(result))
			else:
				value = result.eval() 
				if not isinstance(result, Statement):
					print(value)