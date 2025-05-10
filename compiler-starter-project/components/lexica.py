from sly import Lexer
import sly

class MyLexer(Lexer):
    tokens = {
        ASSIGN, NAME, NUMBER, FLOAT, STRING, TRUE, FALSE,
        EQ, NEQ, MINUS, DIVIDE, TIMES, LPAREN, RPAREN,
        IF, THEN, ELSE, WHILE, DO, END, FUN, RETURN, PRINT
    }
    literals = { '+', ',' }

    ignore = ' \t'
    ignore_newline = r'\n+'

    IF = r'if'
    THEN = r'then'
    ELSE = r'else'
    WHILE = r'while'
    DO = r'do'
    END = r'end'
    FUN = r'fun'
    RETURN = r'return'
    PRINT = r'print'
    TRUE = r'true'
    FALSE = r'false'

    # Ensure EQ and NEQ are matched before ASSIGN
    EQ = r'=='
    NEQ = r'!='
    ASSIGN = r'='  # This should match only a single =, after EQ/NEQ

    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\d+\.\d+')
    def FLOAT(self, token):
        token.value = float(token.value)
        return token

    @_(r'\d+')
    def NUMBER(self, token):
        token.value = int(token.value)
        return token

    @_(r'"[^"]*"')
    def STRING(self, token):
        token.value = token.value[1:-1]
        return token

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"ERROR: Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1

    def tokenize(self, text, lineno=1, index=0):
        tokens = super().tokenize(text, lineno, index)
        token_types = []
        tokens_list = []
        for token in tokens:
            token_types.append(token.type)
            tokens_list.append(token)
        print(f"DEBUG: Tokens generated: {token_types}")
        return iter(tokens_list)