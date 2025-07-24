from enum import Enum

class TokenType(Enum):
    DEF = 1,
    LEFT_BRACE = 2,
    RIGHT_BRACE = 3
    LEFT_PAREN = 4
    RIGHT_PAREN = 5
    LEFT_BRACKET = 6
    RIGHT_BRACKET = 7
    LET = 8
    COMMA = 9
    SEMICOLON = 10
    EQUAL = 11
    ARROW = 12
    TRANSFORM = 13
    IDENTIFIER = 14
    EOF = 15

class Token:
    def __init__(self, ttype: TokenType, value: str):
        self.type = ttype
        self.value = value

    def __repr__(self):
        return f"<{self.type}: {self.value}>"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.tokens = []

    def read_tokens(self):
        while not self.is_at_end():
            c = self.peek()

            match c:
                case '(':
                    self.tokens.append(Token(TokenType.LEFT_PAREN, c))
                    self.advance()
                case ')':
                    self.tokens.append(Token(TokenType.RIGHT_PAREN, c))
                    self.advance()
                case '{':
                    self.tokens.append(Token(TokenType.LEFT_BRACE, c))
                    self.advance()
                case '}':
                    self.tokens.append(Token(TokenType.RIGHT_BRACE, c))
                    self.advance()
                case '[':
                    self.tokens.append(Token(TokenType.LEFT_BRACKET, c))
                    self.advance()
                case ']':
                    self.tokens.append(Token(TokenType.RIGHT_BRACKET, c))
                    self.advance()
                case '-':
                    if self.peek_next() == '>':
                        # Technically c is the incorrect value to use here, but all arrows are the same anyway
                        self.tokens.append(Token(TokenType.ARROW, c))
                        self.advance(2)
                case ',':
                    self.tokens.append(Token(TokenType.COMMA, c))
                    self.advance()
                case ';':
                    self.tokens.append(Token(TokenType.SEMICOLON, c))
                    self.advance()
                case '=':
                    self.tokens.append(Token(TokenType.EQUAL, c))
                    self.advance()
                case ' ':
                    self.advance()
                    continue
                case '\n':
                    self.advance()
                    continue
                case _:
                    self.read_identifier()
        self.tokens.append(Token(TokenType.EOF, '\0'))

    def read_identifier(self):
        letters = []

        while not self.is_at_end():
            c = self.peek()
            if c.isdigit() or c.isalpha():
                self.advance()
                letters.append(c)
            else:
                break
        ident = ''.join(letters)

        match ident:
            case 'let':
                self.tokens.append(Token(TokenType.LET, ident))
            case 'def':
                self.tokens.append(Token(TokenType.DEF, ident))
            case 'transform':
                self.tokens.append(Token(TokenType.TRANSFORM, ident))
            case _:
                self.tokens.append(Token(TokenType.IDENTIFIER, ident))


    def advance(self, n=1):
        self.pos += n

    def peek(self):
        return self.source[self.pos]

    def peek_next(self):
        return self.source[self.pos + 1]

    def is_at_end(self):
        return self.pos >= len(self.source)