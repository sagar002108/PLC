import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QLCDNumber, QMessageBox
from components.lexica import MyLexer
from components.parsers import ASTParser
from components.memory import Memory
from components.ast.statement import ExpressionNumber, ExpressionFloat, ExpressionString, ExpressionBoolean
import io
from contextlib import redirect_stdout

print("DEBUG: Importing Memory")
try:
    memory_test = Memory()
    print(f"DEBUG: Memory import successful: {memory_test}")
except NameError as ne:
    print(f"DEBUG: NameError on Memory import: {ne}")

class MainWindow(QMainWindow):
    input_text: QTextEdit
    output_text: QTextEdit
    output_lcd: QLCDNumber
    button_1: QPushButton
    button_2: QPushButton
    button_plus: QPushButton
    button_minus: QPushButton
    button_times: QPushButton
    button_divide: QPushButton
    button_eq: QPushButton
    button_neq: QPushButton
    button_assign: QPushButton
    button_lparen: QPushButton
    button_rparen: QPushButton
    button_quote: QPushButton
    button_true: QPushButton
    button_false: QPushButton
    button_if: QPushButton
    button_then: QPushButton
    button_else: QPushButton
    button_end: QPushButton
    button_while: QPushButton
    button_do: QPushButton
    button_fun: QPushButton
    button_return: QPushButton
    button_print: QPushButton
    button_clear: QPushButton
    button_equal: QPushButton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./components/main.ui", self)

        self.button_1.clicked.connect(lambda: self.push("1"))
        self.button_2.clicked.connect(lambda: self.push("2"))
        self.button_plus.clicked.connect(lambda: self.push("+"))
        self.button_minus.clicked.connect(lambda: self.push("-"))
        self.button_times.clicked.connect(lambda: self.push("*"))
        self.button_divide.clicked.connect(lambda: self.push("/"))
        self.button_eq.clicked.connect(lambda: self.push("=="))
        self.button_neq.clicked.connect(lambda: self.push("!="))
        self.button_assign.clicked.connect(lambda: self.push("="))
        self.button_lparen.clicked.connect(lambda: self.push("("))
        self.button_rparen.clicked.connect(lambda: self.push(")"))
        self.button_quote.clicked.connect(lambda: self.push('"'))
        self.button_true.clicked.connect(lambda: self.push("true"))
        self.button_false.clicked.connect(lambda: self.push("false"))
        self.button_if.clicked.connect(lambda: self.push("if "))
        self.button_then.clicked.connect(lambda: self.push("then\n"))
        self.button_else.clicked.connect(lambda: self.push("else\n"))
        self.button_end.clicked.connect(lambda: self.push("end\n"))
        self.button_while.clicked.connect(lambda: self.push("while "))
        self.button_do.clicked.connect(lambda: self.push("do\n"))
        self.button_fun.clicked.connect(lambda: self.push("fun "))
        self.button_return.clicked.connect(lambda: self.push("return "))
        self.button_print.clicked.connect(lambda: self.push("print "))
        self.button_clear.clicked.connect(self.clear)
        self.button_equal.clicked.connect(self.execute)  # Connect to execute, not push_equal

    def push(self, text: str):
        current_text = self.input_text.toPlainText()
        self.input_text.setPlainText(current_text + text)

    def clear(self):
        self.input_text.clear()
        self.output_text.clear()
        self.output_lcd.display(0)

    def execute(self):
        try:
            output_stream = io.StringIO()
            with redirect_stdout(output_stream):
                print("DEBUG: Starting execution")
                lexer = MyLexer()
                print("DEBUG: Lexer created")
                parser = ASTParser()
                print("DEBUG: Parser created")
                memory = Memory()
                print(f"DEBUG: Memory instantiated: {memory}")
                input_text = self.input_text.toPlainText()  # Use toPlainText(), not text()
                print(f"DEBUG: Input text: {input_text}")
                tokens = lexer.tokenize(input_text)
                program = parser.parse(tokens)
                print(f"DEBUG: Program parsed: {program}")
                result = None
                for stmt in program:
                    print(f"DEBUG: Executing statement: {stmt}")
                    stmt.run(memory)
                    if isinstance(stmt, (ExpressionNumber, ExpressionFloat, ExpressionString, ExpressionBoolean)):
                        result = stmt.value
                print(f"DEBUG: Execution complete, result: {result}")
                if isinstance(result, (int, float)):
                    self.output_lcd.display(result)
                    print(f"DEBUG: LCD displaying: {result}")
                else:
                    self.output_lcd.display(0)
                    print("DEBUG: LCD reset to 0")
            print("DEBUG: Setting output text")
            self.output_text.setPlainText(output_stream.getvalue())
            print("DEBUG: Output text set")
        except NameError as ne:
            print(f"DEBUG: NameError caught: {ne}")
            QMessageBox.critical(self, "Error", f"NameError: {ne}")
        except Exception as e:
            print(f"DEBUG: Exception caught: {e}")
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()