from sly import Parser
from components.lexica import MyLexer
from components.memory import Memory
from components.ast.statement import (
    Operations, ExpressionNumber, ExpressionFloat, ExpressionString, ExpressionBoolean,
    ExpressionMath, ExpressionVariable, AssignmentStatement, IfStatement, WhileStatement,
    FunctionDefinition, FunctionCall, PrintStatement, ReturnStatement
)

class ASTParser(Parser):
    debugfile = 'parser.out'
    start = 'program'
    tokens = MyLexer.tokens
    precedence = (
        ('left', EQ, NEQ),
        ('left', '+', MINUS),
        ('left', TIMES, DIVIDE),
    )

    def __init__(self):
        self.memory = Memory()

    @_('statements')
    def program(self, p) -> list:
        return p.statements

    @_('statement statements')
    def statements(self, p) -> list:
        return [p.statement] + p.statements

    @_('')
    def statements(self, p) -> list:
        return []

    @_('NAME ASSIGN expr')
    def statement(self, p):
        return AssignmentStatement(p.NAME, p.expr)

    @_('IF expr THEN statements ELSE statements END')
    def statement(self, p):
        return IfStatement(p.expr, p.statements0, p.statements1)

    @_('WHILE expr DO statements END')
    def statement(self, p):
        return WhileStatement(p.expr, p.statements)

    @_('FUN NAME LPAREN params RPAREN statements END')
    def statement(self, p):
        return FunctionDefinition(p.NAME, p.params, p.statements)

    @_('PRINT expr')
    def statement(self, p):
        return PrintStatement(p.expr)

    @_('RETURN expr')
    def statement(self, p):
        return ReturnStatement(p.expr)

    @_('NAME')
    def param(self, p) -> str:
        return p.NAME

    @_('param "," params')
    def params(self, p) -> list:
        return [p.param] + p.params

    @_('param')
    def params(self, p) -> list:
        return [p.param]

    @_('')
    def params(self, p) -> list:
        return []

    @_('expr "+" expr')
    def expr(self, p):
        return ExpressionMath(Operations.PLUS, p.expr0, p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return ExpressionMath(Operations.MINUS, p.expr0, p.expr1)

    @_('expr TIMES expr')
    def expr(self, p):
        return ExpressionMath(Operations.TIMES, p.expr0, p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return ExpressionMath(Operations.DIVIDE, p.expr0, p.expr1)

    @_('expr EQ expr')
    def expr(self, p):
        return ExpressionMath(Operations.EQ, p.expr0, p.expr1)

    @_('expr NEQ expr')
    def expr(self, p):
        return ExpressionMath(Operations.NEQ, p.expr0, p.expr1)

    @_('NUMBER')
    def expr(self, p):
        return ExpressionNumber(p.NUMBER)

    @_('FLOAT')
    def expr(self, p):
        return ExpressionFloat(p.FLOAT)

    @_('STRING')
    def expr(self, p):
        return ExpressionString(p.STRING)

    @_('TRUE')
    def expr(self, p):
        return ExpressionBoolean(True)

    @_('FALSE')
    def expr(self, p):
        return ExpressionBoolean(False)

    @_('NAME')
    def expr(self, p):
        return ExpressionVariable(p.NAME)

    @_('NAME LPAREN args RPAREN')
    def expr(self, p):
        return FunctionCall(p.NAME, p.args)

    @_('expr "," args')
    def args(self, p) -> list:
        return [p.expr] + p.args

    @_('expr')
    def args(self, p) -> list:
        return [p.expr]

    @_('')
    def args(self, p) -> list:
        return []

    def error(self, p):
        if p:
            print(f"DEBUG: Syntax error at token {p.type} (value: {p.value}) at line {p.lineno}")
        else:
            print("DEBUG: Syntax error at EOF")