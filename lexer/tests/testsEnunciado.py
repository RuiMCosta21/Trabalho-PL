import doctest
from lexer.tests.fortranLexer import fortranLexer

def test_lexer(input_text):
    """
    Utility function to verify loop tokenization.

    Examples:
    ---------
    >>> # 1. Hello World (Testing Literals and Print)
    >>> hello = '''      PROGRAM HELLO
    ...       PRINT *, 'Ola, Mundo!'
    ...       END'''
    >>> test_lexer(hello)
    ['PROGRAM', 'IDEN', 'PRINT', '*', ',', 'CHARACTER', 'END']

    >>> # 2. Factorial (Testing DO loops and Labels)
    >>> factorial = '''      PROGRAM FATORIAL
    ...       INTEGER N, I, FAT
    ...       FAT = 1
    ...       DO 10 I = 1, N
    ...       FAT = FAT * I
    ... 10    CONTINUE
    ...       END'''
    >>> test_lexer(factorial)
    ['PROGRAM', 'IDEN', 'INT_IDEN', 'IDEN', ',', 'IDEN', ',', 'IDEN', 'IDEN', '=', 'INT', \
'DO', 'LABEL', 'IDEN', '=', 'INT', ',', 'IDEN', 'IDEN', '=', 'IDEN', '*', 'IDEN', \
'LABEL', 'CONTINUE', 'END']
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