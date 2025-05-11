import sys
import traceback
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
    button_clear: QPushButton
    button_equal: QPushButton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./components/main.ui", self)

        self.button_clear.clicked.connect(self.clear)
        self.button_equal.clicked.connect(self.execute)

    def clear(self):
        self.input_text.clear()
        self.output_text.clear()
        self.output_lcd.display(0)
        memory = Memory()
        memory.memory.clear()
        print("DEBUG: Memory cleared")

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
                input_text = self.input_text.toPlainText()
                print(f"DEBUG: Input text: {input_text}")
                tokens = lexer.tokenize(input_text)
                token_list = list(tokens)
                print(f"DEBUG: Tokens: {[t.type + ':' + str(t.value) for t in token_list]}")
                program = parser.parse(iter(token_list))
                print(f"DEBUG: Program parsed: {program}")
                result = None
                for stmt in program:
                    print(f"DEBUG: Executing statement: {stmt}")
                    stmt.run(memory)
                    if isinstance(stmt, (ExpressionNumber, ExpressionFloat, ExpressionString, ExpressionBoolean)):
                        result = stmt.run(memory)
                    print(f"DEBUG: Memory after statement: {memory}")
                print(f"DEBUG: Execution complete, result: {result}")
                if isinstance(result, (int, float)):
                    self.output_lcd.display(result)
                    print(f"DEBUG: LCD displaying: {result}")
                elif isinstance(result, bool):
                    self.output_text.append(str(result).lower())
                    print(f"DEBUG: Output text appending: {result}")
                else:
                    self.output_lcd.display(0)
                    print("DEBUG: LCD reset to 0")
            print("DEBUG: Setting output text")
            self.output_text.setPlainText(output_stream.getvalue())
            print("DEBUG: Output text set")
        except NameError as ne:
            print(f"DEBUG: NameError caught: {ne}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"NameError: {ne}")
        except Exception as e:
            print(f"DEBUG: Exception caught: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()