import doctest
from lexer.tests.fortranLexer import fortranLexer

def test_lexer(input_text):
    """
    Utility function to tokenize a string and return a list of token types 
    and values for doctest verification.

    Examples:
    ---------
    >>> # Testing basic Control Flow (Standard 6-space margin)
    >>> test_lexer("      IF (X .GT. 0) THEN")
    ['IF', '(', 'IDEN', 'GREATERTHAN', 'INT', ')', 'THEN']

    >>> # Testing Loops (The label 10 follows the DO keyword)
    >>> test_lexer("      DO 10 I = 1, 100")
    ['DO', 'LABEL', 'IDEN', '=', 'INT', ',', 'INT']

    >>> # Testing Subroutines and Common Blocks (Multiple lines, both with margins)
    >>> test_lexer("      SUBROUTINE CALC()\\n      COMMON /DATA/ X, Y")
    ['SUBROUTINE', 'IDEN', '(', ')', 'COMMON', 'SEPARATOR', 'IDEN', 'SEPARATOR', 'IDEN', ',', 'IDEN']

    >>> # Testing Memory and Data
    >>> test_lexer("      DIMENSION A(10)\\n      DATA A /10 * 0.0/")
    ['DIMENSION', 'IDEN', '(', 'INT', ')', 'DATA', 'IDEN', 'SEPARATOR', 'INT', 'MULT', 'REAL', 'SEPARATOR']

    >>> # Testing Labels in Columns 1-5
    >>> # Note: 100 is in the label zone, FORMAT starts in Column 7
    >>> test_lexer("100   FORMAT(I5, F10.2)")
    ['LABEL', 'FORMAT', '(', 'FORMAT_CODE', ',', 'FORMAT_CODE', ')']

    >>> # Testing Comments and Control Flow
    >>> # The 'C' in Column 1 should cause the entire first line to be ignored
    >>> test_lexer("C     THIS IS A COMMENT\\n      ELSEIF (A .EQ. B) GOTO 20")
    ['ELSEIF', '(', 'IDEN', 'EQ', 'IDEN', ')', 'GOTO', 'LABEL']

    >>> # Testing Continuation (Character in Column 6)
    >>> # Line 1 sets up an assignment; Line 2 continues it
    >>> test_lexer("      X = 5 + \\n     & 10")
    ['IDEN', '=', 'INT', 'ADD', 'INT']
    """
    fortranLexer.input(input_text)

    fortranLexer.begin('startLine')
    fortranLexer.do_label_flag = False
    fortranLexer.separator_flag = False
    fortranLexer.line_start = 0
    fortranLexer.previous_state = "INITIAL"
    #print([(tok.type, tok.value, tok.lineno, tok.lexpos) for tok in fortranLexer])
    return [(tok.type) for tok in fortranLexer]

doctest.run_docstring_examples(test_lexer, globals())

