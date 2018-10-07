import re

EOF = "EOF"
NUMBER = "NUMBER"
OPERATOR = "OPERATOR"
NAME = "NAME"
GROUP_CHAR = "GROUP_CHAR"
COMMA = "COMMA"

class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __repr__(self):
		return f"Token({self.type}, {self.value})"

	def __str__(self):
		return f"{self.type}: {self.value}"

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
	':',
	'!'
]

named_operators = [
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
	'in',
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
	'all'
]

group_chars = [
	'(', ')',
	'[', ']',
	'|', '|',
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
			
			if self.char.isspace():
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
				if name in named_operators:
					result = Token(OPERATOR, name)
				else:
					result = Token(NAME, name)
				self.advance(end - start)
				return result

			if self.char in operator_chars:
				if self.char in ['<', '>', ':', '!'] and self.next_char == '=':
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

			if self.char == ',':
				result = Token(COMMA, self.char)
				self.advance()
				return result

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