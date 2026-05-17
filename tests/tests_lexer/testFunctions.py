import doctest
from lexer.fortranLexer import fortranLexer

def test_lexer(input_text):
    """
    Utility function to verify Subroutine and Function tokenization.

    Examples:
    ---------
    >>> # 1. Simple Subroutine Definition
    >>> test_lexer("      SUBROUTINE UPDATE(X, Y, Z)")
    ['SUBROUTINE', 'IDEN', '(', 'IDEN', ',', 'IDEN', ',', 'IDEN', ')']

    >>> # 2. Typed Function Definition
    >>> # Note: INTEGER_IDEN (or INT_IDEN) should be recognized before FUNCTION
    >>> test_lexer("      INTEGER FUNCTION ADDR(A, B)")
    ['INT_IDEN', 'FUNCTION', 'IDEN', '(', 'IDEN', ',', 'IDEN', ')']

    >>> # 3. Subroutine Call
    >>> test_lexer("      CALL UPDATE(1.0, 2.0, 3.0)")
    ['CALL', 'IDEN', '(', 'REAL', ',', 'REAL', ',', 'REAL', ')']

    >>> # 4. Function Assignment (Identifier vs Keyword)
    >>> # Here ADDR is an identifier receiving a value
    >>> test_lexer("      ADDR = A + B")
    ['IDEN', '=', 'IDEN', '+', 'IDEN']

    >>> # 5. Return and End Statements
    >>> test_lexer("      RETURN\\n      END")
    ['RETURN', 'END']

    >>> # 6. Complex Header with leading label
    >>> # Labels are allowed on the subprogram header, though rare
    >>> test_lexer("100   SUBROUTINE ALPHA")
    ['LABEL', 'SUBROUTINE', 'IDEN']
    """
    fortranLexer.input(input_text)

    fortranLexer.begin('startLine')
    fortranLexer.do_label_flag = False
    fortranLexer.separator_flag = False
    fortranLexer.line_start = 0
    fortranLexer.previous_state = "INITIAL"
    fortranLexer.name_flag = False
    #print([(tok.type, tok.value, tok.lineno, tok.lexpos) for tok in fortranLexer])
    return [(tok.type) for tok in fortranLexer]

doctest.run_docstring_examples(test_lexer, globals())