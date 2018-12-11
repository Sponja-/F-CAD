from tokenizer import *
from elements import *
from arithmetic import *
from algebra import *
from logic import *
from set_theory import *
from statements import *
from flow_control import *
from special_functions import *
from iterable import *
from objects import *
from argparse import ArgumentParser
from pprint import pprint

class Import(Operation):
	def __init__(self, file_path):
		def operation(x):
			try:
				with open(x, 'r') as source_file:
					parse_string(source_file.read())
			except FileNotFoundError:
				ImportPythonModule(String(x)).eval()
		super().__init__(operation, file_path)

power_operators = {
	'^': Exponentiation
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
	'show': Show,
	'import': Import,
	'python': RunPython
}

closing = {
	'[': ']',
	'(': ')',
	'{': '}'
}


debug = False
absolute_assignment_default = True

class Parser:
	assign = AbsoluteAssignment if absolute_assignment_default else Assignment

	def __init__(self, tok_gen):
		self.tokens = list(tok_gen.tokens())
		self.pos = 0
		self.show_errors = True
		self.expr_count = 0

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

	@property
	def prev_token(self):
		if self.pos > 0:
			return self.tokens[self.pos - 1]
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

	def expr_list(self, allow_ellipsis=False):
		if self.token.value in closing.values():
			return []

		if allow_ellipsis and self.token.type == ELLIPSIS:
			self.eat(ELLIPSIS)
			result = [ExpandVector(self.expr())]
		else:
			result = [self.expr()]

		while self.token.type == COMMA:
			self.eat(COMMA)
			if allow_ellipsis and self.token.type == ELLIPSIS:
				self.eat(ELLIPSIS)
				result.append(ExpandVector(self.expr()))
			result.append(self.expr())

		return result

	def name_list(self, allow_ellipsis=False):
		if self.token.type != NAME and self.token.type != ELLIPSIS:
			return []

		if allow_ellipsis and self.token.type == ELLIPSIS:
				self.eat(ELLIPSIS)
				value = (ELLIPSIS, self.token.value)
				self.eat(NAME)
				return [value]

		result = [self.token.value]
		self.eat(NAME)

		while self.token.type == COMMA:
			self.eat(COMMA)
			if allow_ellipsis and self.token.type == ELLIPSIS:
				self.eat(ELLIPSIS)
				result.append((ELLIPSIS, self.token.value))
				self.eat(NAME)
				return result
			result.append(self.token.value)
			self.eat(NAME)

		return result

	def tuple_list(self, allow_ellipsis=False):
		self.eat(GROUP_CHAR, '(')
		result = self.expr_list(allow_ellipsis)
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

		if token.value == "new":
			self.eat(KEYWORD)
			class_name = self.token.value
			self.eat(NAME)
			args = self.tuple_list(True)
			return CreateInstance(class_name, *args)

		if token.value == "null":
			self.eat(KEYWORD)
			return Null(None)

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
		prev_result = None
		while self.token.value in closing.keys() or self.token.type == MEMBER_ACCESS:
			r = result
			if self.token.value == '(':
				arguments = self.tuple_list(True)
				result = MethodCall(prev_result, result, *arguments)
			elif self.token.value == '[':
				indeces = self.vector_constant()
				result = Subscript(result, *indeces)
			elif self.token.type == MEMBER_ACCESS:
				self.eat(MEMBER_ACCESS)
				member_name = self.token.value
				self.eat(NAME)
				result = AccessMember(result, member_name)
			prev_result = r
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
					assignment = self.assignment_statement(absolute_assignment=False)
					assignments[assignment.var.symbol] = assignment.value
			else:
				assignment = self.assignment_statement(absolute_assignment=False)
				assignments = {assignment.var.symbol: assignment.value}
			return Where(result, assignments)
		return result

	def expr(self):
		if debug:
			self.expr_count += 1
		return self.where_expr()

	def assignment_statement(self, **kwargs):
		assign = AbsoluteAssignment if kwargs.get("absolute_assignment", absolute_assignment_default) else Assignment
		start_pos = self.pos

		vars = self.expr_list()
		if self.token.type == ASSIGNMENT:
			self.eat(ASSIGNMENT)
			exprs = self.expr_list()
			assert(len(vars) == len(exprs))
			result = []
			for var, expr in zip(vars, exprs):
				result.append(assign(var, expr))
			if len(result) == 1:
				return result[0]
			return StatementList(result)
		return vars[0] if vars else None

	def return_statement(self):
		if self.token.value == 'return':
			self.eat(KEYWORD)
			return Return(self.assignment_statement())
		return self.assignment_statement()

	def if_else_statement(self):
		if self.token.value == 'if':
			self.eat(KEYWORD)
			self.eat(GROUP_CHAR, '(')
			condition = self.expr()
			self.eat(GROUP_CHAR, ')')
			true_operation = self.statement_block()
			false_operation = None
			if self.token.value == 'else':
				self.eat(KEYWORD, 'else')
				false_operation = self.statement_block()
			return IfElseStatement(condition, true_operation, false_operation)
		return self.return_statement()



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
		return self.if_else_statement()

	def while_statement(self):
		if self.token.value == 'while':
			self.eat(KEYWORD)
			self.eat(GROUP_CHAR, '(')
			condition = self.expr()
			self.eat(GROUP_CHAR, ')')
			operation = self.statement_block()
			return WhileLoop(condition, operation)
		return self.for_statement()

	def function_definition(self):
		if self.token.value == 'function':
			self.eat(KEYWORD)
			name = self.token.value
			self.eat(NAME)
			self.eat(GROUP_CHAR, '(')
			args = self.name_list(True)
			self.eat(GROUP_CHAR, ')')
			var_arg_symbol = None
			if args and type(args[-1]) == tuple and args[-1][0] == ELLIPSIS:
				var_arg_symbol = args.pop()[1]
			if self.token.type == ASSIGNMENT:
				self.eat(ASSIGNMENT)
			return Parser.assign(Variable(name), Function(args, self.statement_block(scoped=True), var_arg_symbol))
		return self.while_statement()

	def class_definition(self):
		if self.token.value == 'class':
			self.eat(KEYWORD)
			name = self.token.value
			self.eat(NAME)
			parent_name = None
			if self.token.value == 'extends':
				self.eat(KEYWORD)
				parent_name = self.token.value
				self.eat(NAME)
			definitions = self.statement_block(force_block=True)
			attributes = {}
			for assignment in definitions.statements:
				assert(type(assignment) is Parser.assign)
				attributes[assignment.var.symbol] = assignment.expr
			return ClassDefinition(name, parent_name, attributes)
		return self.function_definition()

	def statement(self):
		return self.class_definition()

	def statement_list(self, **kwargs):
		s = self.statement()
		result = [s] if s is not None else []
		while self.token.value != '}' and self.token.type != EOF:
			if self.prev_token.value != '}':
				self.eat(SEMICOLON)
			s = self.statement()
			if s is not None:
				if debug: print(str(s))
				result.append(s)
		return ScopedStatements(result) if kwargs.get("scoped", False) else StatementList(result)

	def statement_block(self, **kwargs):
		if self.token.value != '{' and not kwargs.get("force_block", False):
			return self.statement()
		self.eat(GROUP_CHAR)
		result = self.statement_list(**kwargs)
		self.eat(GROUP_CHAR, '}')
		return result

def parse_string(s):
	Parser(Tokenizer(s.strip())).statement_list().eval()


if __name__ == '__main__':
	Import(String("default_import")).eval()
	parser = ArgumentParser(description="Interprets a file, or works as a REPL if none is provided")
	parser.add_argument('file', type=str, help='File to interpret', nargs='?')

	args = parser.parse_args()

	if args.file is not None:
		with open(args.file, 'r') as file:
			parse_string(file.read())
	else:
		while True:
			result = Parser(Tokenizer(input('> '))).statement()
			if debug:
				print(str(result))
			else:
				value = result.eval() 
				if not isinstance(result, Statement):
					print(value)