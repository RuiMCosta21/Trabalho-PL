import doctest
from lexer.tests.fortranLexer import fortranLexer

def test_lexer(input_text):
    """
    >>> # Testing a block of multiple comment lines
    >>> multi_line_comment = '''C     LINE ONE OF COMMENT
    ... * LINE TWO OF COMMENT
    ... c     LINE THREE OF COMMENT
    ...       X = 10'''
    >>> test_lexer(multi_line_comment)
    ['IDEN', '=', 'INT']

    >>> # Testing comments interspersed with code
    >>> mixed_comments = '''      X = 5
    ... C     INTERMEDIATE COMMENT
    ...       Y = 10
    ... * FINAL COMMENT'''
    >>> test_lexer(mixed_comments)
    ['IDEN', 'ASSIGN', 'NUM', 'IDEN', 'ASSIGN', 'NUM']

    >>> # Testing a standard comment starting with 'C' in Column 1
    >>> test_lexer("C     THIS IS A COMMENT\\n      IF (X .GT. 0) THEN")
    ['IF', '(', 'IDEN', 'GT', 'NUM', ')', 'THEN']

    >>> # Testing a comment starting with '*' in Column 1
    >>> test_lexer("* ANOTHER COMMENT STYLE\\n      GOTO 10")
    ['GOTO', 'LABEL']

    >>> # Testing lowercase 'c' in Column 1
    >>> test_lexer("c     lower case comment\\n      RETURN")
    ['RETURN']

    >>> # Testing an empty comment line (just the 'C')
    >>> test_lexer("C\\n      ENDIF")
    ['ENDIF']

    >>> # Testing that a 'C' in the mIDENdle of a line is NOT a comment (it's an IDEN)
    >>> test_lexer("      X = C + 1")
    ['IDEN', 'ASSIGN', 'IDEN', 'PLUS', 'INT']
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