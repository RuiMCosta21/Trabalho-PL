import doctest
from lexer.tests.fortranLexer import fortranLexer

def test_lexer(input_text):
    """
    Utility function to verify loop tokenization.

    Examples:
    ---------
    >>> # 1. Standard DO loop with a 6-space margin
    >>> # DO is a keyword, 20 is a LABEL (due to the DO rule), I is IDEN
    >>> test_lexer("      DO 20 I = 1, 10")
    ['DO', 'LABEL', 'IDEN', '=', 'INT', ',', 'INT']

    >>> # 2. DO loop with a step value (increment)
    >>> test_lexer("      DO 30 K = 10, 0, -1")
    ['DO', 'LABEL', 'IDEN', '=', 'INT', ',', 'INT', ',', 'INT']

    >>> # 3. Nested Loops with a terminal CONTINUE statement
    >>> # This tests multi-line state transitions and labels in columns 1-5
    >>> nested_loop = '''      DO 100 I = 2, 5
    ...       DO 200 J = 1, 5
    ... 200   CONTINUE
    ... 100   CONTINUE'''
    >>> test_lexer(nested_loop)
    ['DO', 'LABEL', 'IDEN', '=', 'INT', ',', 'INT', 'DO', 'LABEL', 'IDEN', '=', 'INT', ',', 'INT', 'LABEL', 'CONTINUE', 'LABEL', 'CONTINUE']

    >>> # 4. The "Labeled DO" - A label on the DO statement itself
    >>> # '10' is a label definition (col 1-5), '50' is a label reference (loop target)
    >>> test_lexer("10    DO 50 J = 1, 10")
    ['LABEL', 'DO', 'LABEL', 'IDEN', '=', 'INT', ',', 'INT']

    >>> # 5. DO WHILE loop (Fortran 77 extension)
    >>> test_lexer("      DO WHILE (X .GT. 0)")
    ['DO', 'WHILE', '(', 'IDEN', 'GREATERTHAN', 'INT', ')']
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