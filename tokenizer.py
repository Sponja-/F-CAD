import re

EOF = -1
NUMBER = 0
OPERATOR = 1
NAME = 2
GROUP_CHAR = 3
COMMA = 4
SEMICOLON = 5
SEPARATOR = 6
QUESTION = 7
ASSIGNMENT = 8
RANGE = 9
KEYWORD = 10

names = {
	EOF: "EOF",
	NUMBER: "NUMBER",
	OPERATOR: "OPERATOR",
	NAME: "NAME",
	GROUP_CHAR: "GROUP_CHAR",
	COMMA: "COMMA",
	SEMICOLON: "SEMICOLON",
	SEPARATOR: "SEPARATOR",
	QUESTION: "QUESTION",
	ASSIGNMENT: "ASSIGNMENT",
	RANGE: "RANGE",
	KEYWORD: "KEYWORD"
}

special_chars = {
	',': COMMA,
	'\n': SEMICOLON,
	'|': SEPARATOR,
	'?': QUESTION,
}

class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __repr__(self):
		return f"Token({names[self.type]}, {self.value})"

	def __str__(self):
		return f"{names[self.type]}: {self.value}"

number_regex = re.compile(r"^([+-]?([0-9]+)(\.([0-9]+))?)")
name_regex = re.compile(r"^([A-Za-z_][A-Za-z_0-9]*)")

operator_chars = [
	'+',
	'-',
	'*',
	'/',
	'^',
	'%',
	'.',
	'<',
	'>',
	'=',
	'!',
	'.',
	':'
]

keywords = [
	'for',
	'in',
	'otherwise',
	'where'
]

named = [
	'sqrt',
	'root',
	'log',
	'ln',
	'lg',
	'inv',
	'abs',
	'row',
	'col',
	'P',
	'C',
	'sin',
	'cos',
	'tan',
	'arcsin',
	'arccos',
	'arctan',
	'and',
	'or',
	'not',
	'xor',
	'any',
	'all',
	'diff',
	'print',
	'graph',
	'scatter',
	'show',
	'take',
	'tail',
	'union',
	'intersection',
	'len',
	'slice',
	'input'
]

group_chars = [
	'(', ')',
	'[', ']',
	'{', '}'
]

class Tokenizer:
	def __init__(self, text):
		self.text = text + '\0'
		self.pos = 0

	@property
	def char(self):
		return self.text[self.pos]

	@property
	def next_char(self):
		return self.text[self.pos + 1]

	def advance(self, amount = 1):
		self.pos += amount

	def skip_whitespace(self):
		while self.char != '\0' and self.char.isspace():
			self.advance()

	def get_next_token(self):
		while self.char != '\0':
			
			if self.char.isspace() and self.char != '\n':
				self.skip_whitespace()
				continue

			number_match = number_regex.match(self.text[self.pos:])
			if number_match is not None:
				start, end = number_match.span()
				result = Token(NUMBER, float(self.text[self.pos + start:self.pos + end]))
				self.advance(end - start)
				return result

			name_match = name_regex.match(self.text[self.pos:])
			if name_match is not None:
				start, end = name_match.span()
				name = self.text[self.pos + start: self.pos + end]
				if name in keywords:
					result = Token(KEYWORD, name)
				elif name in named:
					result = Token(OPERATOR, name)
				else:
					result = Token(NAME, name)
				self.advance(end - start)
				return result

			if self.char == '.' and self.next_char == '.':
				self.advance(2)
				return Token(RANGE, '..')

			if self.char == ':' and self.next_char == '=':
				self.advance(2)
				return Token(ASSIGNMENT, ':=')

			if self.char in operator_chars:
				if self.char in ['<', '>', '!', '='] and self.next_char == '=':
					result = Token(OPERATOR, self.char + self.next_char)
					self.advance(2)
					return result
				result = Token(OPERATOR, self.char)
				self.advance()
				return result

			if self.char in group_chars:
				result = Token(GROUP_CHAR, self.char)
				self.advance()
				return result

			if self.char in special_chars:
				result = Token(special_chars[self.char], self.char)
				self.advance()
				return result

			if self.char == '\\' and self.next_char == '\n':
				self.advance(2)
				continue

			raise SyntaxError

		return Token(EOF, '\0')

	def tokens(self):
		token = self.get_next_token()
		while token.type != EOF:
			yield token
			token = self.get_next_token()
		yield token

if __name__ == '__main__':
	inp = input('> ')
	while inp != '':
		t = Tokenizer(inp)
		print("\n".join(str(tok) for tok in t.tokens()) + '\n')
		inp = input('> ')