from parser.fortranParser import fortranParser
from lexer.fortranLexer import fortranLexer
from parser.SymbolTable import SymbolTable
from parser.SemanticError import SemanticError
from codeGen.EVMCodeGenerator import CodeGenerator

import sys

def parse_file(file_path):
    with open(file_path, "r") as f:
        text = f.read()

    fortranLexer.begin('startLine')
    fortranLexer.do_label_flag = False
    fortranLexer.separator_flag = False
    fortranLexer.line_start = 0
    fortranLexer.previous_state = "INITIAL"
    fortranLexer.name_flag = False

    fortranParser.symbols = SymbolTable()
    fortranParser.codegen = CodeGenerator(fortranParser.symbols)

    try:
        code = fortranParser.parse(text, lexer=fortranLexer)
        print("Program is syntactically correct")
        print("Execute in EWVM:\n")
        print("\n".join(code))

    except SyntaxError as e:
        print("Parsing failed:", e)

    except SemanticError as e:
        print("Parsing failed:", e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <input_file>")
        sys.exit(1)

    parse_file(sys.argv[1])
