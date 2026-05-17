import doctest
from lexer.fortranLexer import fortranLexer

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
    ['PROGRAM', 'NAME', 'PRINT', '*', ',', 'CHARACTER', 'END']

    >>> # 2. Factorial (Testing DO loops and Labels)
    >>> factorial = '''      PROGRAM FATORIAL
    ...       INTEGER N, I, FAT
    ...       FAT = 1
    ...       DO 10 I = 1, N
    ...       FAT = FAT * I
    ... 10    CONTINUE
    ...       END'''
    >>> test_lexer(factorial)
    ['PROGRAM', 'NAME', 'INT_IDEN', 'IDEN', ',', 'IDEN', ',', 'IDEN', 'IDEN', '=', 'INT', \
'DO', 'LABEL', 'IDEN', '=', 'INT', ',', 'IDEN', 'IDEN', '=', 'IDEN', '*', 'IDEN', \
'LABEL', 'CONTINUE', 'END']

    >>> # 3. PRIMO
    >>> # Verifies labels, logical operators, and intrinsic function calls (MOD)
    >>> program_primo = '''      PROGRAM PRIMO
    ...       INTEGER NUM, I
    ...       LOGICAL ISPRIM
    ...       PRINT *, 'Introduza um numero inteiro positivo:'
    ...       READ *, NUM
    ...       ISPRIM = .TRUE.
    ...       I = 2
    ... 20    IF (I .LE. (NUM/2) .AND. ISPRIM) THEN
    ...         IF (MOD(NUM, I) .EQ. 0) THEN
    ...             ISPRIM = .FALSE.
    ...         ENDIF
    ...       I = I + 1
    ...       GOTO 20
    ...       ENDIF
    ...       IF (ISPRIM) THEN
    ...         PRINT *, NUM, ' e um numero primo'
    ...       ELSE
    ...         PRINT *, NUM, ' nao e um numero primo'
    ...       ENDIF
    ...       END'''
    >>> test_lexer(program_primo)
    ['PROGRAM', 'NAME', 'INT_IDEN', 'IDEN', ',', 'IDEN', 'LOGICAL_IDEN', 'IDEN', \
'PRINT', '*', ',', 'CHARACTER', 'READ', '*', ',', 'IDEN', 'IDEN', '=', 'LOGICAL', \
'IDEN', '=', 'INT', 'LABEL', 'IF', '(', 'IDEN', 'LESSEQ', '(', 'IDEN', 'DIV', 'INT', ')', \
'AND', 'IDEN', ')', 'THEN', 'IF', '(', 'IDEN', '(', 'IDEN', ',', 'IDEN', ')', 'EQ', \
'INT', ')', 'THEN', 'IDEN', '=', 'LOGICAL', 'ENDIF', 'IDEN', '=', 'IDEN', '+', 'INT', \
'GOTO', 'LABEL', 'ENDIF', 'IF', '(', 'IDEN', ')', 'THEN', 'PRINT', '*', ',', 'IDEN', \
',', 'CHARACTER', 'ELSE', 'PRINT', '*', ',', 'IDEN', ',', 'CHARACTER', 'ENDIF', 'END']

    >>> # 4. Soma de uma lista de inteiros
    >>> sum = '''      PROGRAM SOMAARR
    ...       INTEGER NUMS(5)
    ...       INTEGER I, SOMA
    ...       SOMA = 0
    ...       PRINT *, 'Introduza 5 numeros inteiros:'
    ...       DO 30 I = 1, 5
    ...       READ *, NUMS(I)
    ...       SOMA = SOMA + NUMS(I)
    ... 30    CONTINUE
    ...       PRINT *, 'A soma dos numeros e: ', SOMA
    ...       END'''
    >>> test_lexer(sum)
    ['PROGRAM', 'NAME', 'INT_IDEN', 'IDEN', '(', 'INT', ')', 'INT_IDEN', 'IDEN', ',', 'IDEN', \
'IDEN', '=', 'INT', 'PRINT', '*', ',', 'CHARACTER', 'DO', 'LABEL', 'IDEN', '=', 'INT', ',', 'INT', \
'READ', '*', ',', 'IDEN', '(', 'IDEN', ')', 'IDEN', '=', 'IDEN', '+', 'IDEN', '(', 'IDEN', ')', \
'LABEL', 'CONTINUE', 'PRINT', '*', ',', 'CHARACTER', ',', 'IDEN', 'END']
    """    
    fortranLexer.input(input_text)

    fortranLexer.begin('startLine')
    fortranLexer.do_label_flag = False
    fortranLexer.separator_flag = False
    fortranLexer.line_start = 0
    fortranLexer.previous_state = "INITIAL"
    fortranLexer.name_flag = False
    print([(tok.type, tok.value) for tok in fortranLexer])
    return [(tok.type) for tok in fortranLexer]

doctest.run_docstring_examples(test_lexer, globals())
