from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Optional
from components.memory import Memory

class Operations(Enum):
    PLUS = 0
    MINUS = 1
    TIMES = 2
    DIVIDE = 3
    EQ = 4
    NEQ = 5
    CONCAT = 6

class Expression(ABC):
    @abstractmethod
    def __init__(self):
        self.value = None
        self.signature: str = ""

    @abstractmethod
    def run(self, memory) -> None:
        pass

class ExpressionNumber(Expression):
    def __init__(self, number: int):
        self.value = number
        self.signature = str(number)

    def run(self, memory) -> None:
        pass

    def __repr__(self) -> str:
        return f"Number:{self.value}"

class ExpressionFloat(Expression):
    def __init__(self, number: float):
        self.value = number
        self.signature = str(number)

    def run(self, memory) -> None:
        pass

    def __repr__(self) -> str:
        return f"Float:{self.value}"

class ExpressionString(Expression):
    def __init__(self, string: str):
        self.value = string
        self.signature = f'"{string}"'

    def run(self, memory) -> None:
        pass

    def __repr__(self) -> str:
        return f"String:{self.signature}"

class ExpressionBoolean(Expression):
    def __init__(self, value: bool):
        self.value = value
        self.signature = str(value).lower()

    def run(self, memory) -> None:
        pass

    def __repr__(self) -> str:
        return f"Boolean:{self.value}"

class ExpressionMath(Expression):
    def __init__(self, operation: Operations, parameter1: Expression, parameter2: Expression):
        self.operation = operation
        self.parameter1 = parameter1
        self.parameter2 = parameter2
        self.signature = ""
        self.value = None
        self.children = [parameter1, parameter2]

    def run(self, memory) -> None:
        try:
            # Run children to compute their values
            for child in self.children:
                child.run(memory)
                if child.value is None:
                    raise ValueError(f"Child expression {child} has no value after run")

            # Ensure values are set
            if self.parameter1.value is None or self.parameter2.value is None:
                raise ValueError(f"Invalid values: parameter1={self.parameter1.value}, parameter2={self.parameter2.value}")

            # Compute based on operation
            if self.operation == Operations.PLUS:
                if isinstance(self.parameter1.value, str) and isinstance(self.parameter2.value, str):
                    self.value = self.parameter1.value + self.parameter2.value
                else:
                    self.value = self.parameter1.value + self.parameter2.value
            elif self.operation == Operations.MINUS:
                self.value = self.parameter1.value - self.parameter2.value
            elif self.operation == Operations.TIMES:
                self.value = self.parameter1.value * self.parameter2.value
            elif self.operation == Operations.DIVIDE:
                self.value = self.parameter1.value / self.parameter2.value
            elif self.operation == Operations.EQ:
                self.value = self.parameter1.value == self.parameter2.value
            elif self.operation == Operations.NEQ:
                self.value = self.parameter1.value != self.parameter2.value
            self.signature = f"{self.operation.name} {self.parameter1.value} {self.parameter2.value}"
        except Exception as e:
            raise ValueError(f"Error computing {self.operation.name} with {self.parameter1} and {self.parameter2}: {e}")

    def __repr__(self) -> str:
        return self.signature

class ExpressionVariable(Expression):
    def __init__(self, name: str):
        self.name = name
        self.signature = name
        self.value = None

    def run(self, memory) -> None:
        self.value = memory.get(self.name)

    def __repr__(self) -> str:
        return f"Variable:{self.name}={self.value}"

class Statement(ABC):
    @abstractmethod
    def run(self, memory) -> None:
        pass

class AssignmentStatement(Statement):
    def __init__(self, variable: str, expression: Expression):
        self.variable = variable
        self.expression = expression

    def run(self, memory) -> None:
        self.expression.run(memory)
        memory.set(self.variable, self.expression.value, type(self.expression.value))

class IfStatement(Statement):
    def __init__(self, condition: Expression, then_block: List[Statement], else_block: List[Statement]):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def run(self, memory) -> None:
        self.condition.run(memory)
        if self.condition.value:
            for stmt in self.then_block:
                stmt.run(memory)
        else:
            for stmt in self.else_block:
                stmt.run(memory)

class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: List[Statement]):
        self.condition = condition
        self.body = body

    def run(self, memory) -> None:
        while True:
            self.condition.run(memory)
            if not self.condition.value:
                break
            for stmt in self.body:
                stmt.run(memory)

class FunctionDefinition(Statement):
    def __init__(self, name: str, params: List[str], body: List[Statement]):
        self.name = name
        self.params = params
        self.body = body

    def run(self, memory) -> None:
        memory.set(self.name, self, FunctionDefinition)

class FunctionCall(Expression):
    def __init__(self, name: str, args: List[Expression]):
        self.name = name
        self.args = args
        self.value = None
        self.signature = f"{name}({','.join(str(arg) for arg in args)})"

    def run(self, memory) -> None:
        func = memory.get(self.name)
        local_memory = Memory()
        for param, arg in zip(func.params, self.args):
            arg.run(memory)
            local_memory.set(param, arg.value, type(arg.value))
        for stmt in func.body:
            stmt.run(local_memory)
        self.value = local_memory.get("return") if "return" in local_memory.memory else None

    def __repr__(self) -> str:
        return f"FunctionCall:{self.signature}"

class PrintStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def run(self, memory) -> None:
        self.expression.run(memory)
        print(str(self.expression.value).lower() if isinstance(self.expression.value, bool) else self.expression.value)

class ReturnStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def run(self, memory) -> None:
        self.expression.run(memory)
        memory.set("return", self.expression.value, type(self.expression.value))