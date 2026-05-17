from parser.fortranParser import fortranParser
from lexer.fortranLexer import fortranLexer
from parser.SymbolTable import SymbolTable
from parser.SemanticError import SemanticError
from codeGen.EVMCodeGenerator import CodeGenerator


def parse(text):
    fortranLexer.begin('startLine')
    fortranLexer.do_label_flag = False
    fortranLexer.separator_flag = False
    fortranLexer.line_start = 0
    fortranLexer.previous_state = "INITIAL"
    fortranLexer.name_flag = False
    fortranParser.symbols = SymbolTable()
    fortranParser.codegen = CodeGenerator(fortranParser.symbols)
    try:
        code = fortranParser.parse(text, lexer=fortranLexer, debug=True)
        fortranParser.symbols.dump()
        print("Program is syntactically correct")
        print("Execute in EWVM:")
        print()
        print("\n".join(code))
    except SyntaxError as e:
        print("Parsing failed:", e)
    except SemanticError as e:
      print("Parsing failed:", e)


# parse("""      PROGRAM HELLO
#       PRINT *, 'Ola, Mundo!'
#       END""")


# parse('''      PROGRAM FATORIAL
#       INTEGER N, I, FAT
#       PRINT *, 'Introduza um numero inteiro positivo:'
#       READ *, N
#       FAT = 1
#       DO 10 I = 1, N
#       FAT = FAT * I
# 10    CONTINUE
#       PRINT *, 'Fatorial de ', N, ': ', FAT
#       END''')

parse('''      PROGRAM PRIMO
      INTEGER NUM, I
      LOGICAL ISPRIM
      PRINT *, 'Introduza um numero inteiro positivo:'
      READ *, NUM
      ISPRIM = .TRUE. 
      I = 2
20    IF (I .LE. (NUM/2) .AND. ISPRIM) THEN
        IF (MOD(NUM, I) .EQ. 0) THEN
            ISPRIM = .FALSE.
        ENDIF
      I = I + 1
      GOTO 20
      ENDIF
      IF (ISPRIM) THEN
        PRINT *, NUM, ' e um numero primo'
      ELSE
        PRINT *, NUM, ' nao e um numero primo'
      ENDIF
      END''')
# 
# parse('''      PROGRAM SOMAARR
#       INTEGER NUMS(5)
#       INTEGER I, SOMA
#       SOMA = 0
#       PRINT *, 'Introduza 5 numeros inteiros:'
#       DO 30 I = 1, 5
#       READ *, NUMS(I)
#       SOMA = SOMA + NUMS(I)
# 30    CONTINUE
#       PRINT *, 'A soma dos numeros e: ', SOMA
#       END''')

# parse('''      PROGRAM CONVERSOR
#       INTEGER NUM, BASE, RESULT, CONVRT
#       PRINT *, 'INTRODUZA UM NUMERO DECIMAL INTEIRO:'
#       READ *, NUM
#       DO 10 BASE = 2, 9
#       RESULT = CONVRT(NUM, BASE)
#       PRINT *, 'BASE ', BASE, ': ', RESULT
# 10    CONTINUE
#       END
#       INTEGER FUNCTION CONVRT(N, B)
#       INTEGER N, B, QUOT, REM, POT, VAL
#       VAL = 0
#       POT = 1
#       QUOT = N
# 20    IF (QUOT .GT. 0) THEN
#       REM = MOD(QUOT, B)
#       VAL = VAL + (REM * POT)
#       QUOT = QUOT / B
#       POT = POT * 10
#       GOTO 20
#       ENDIF
#       CONVRT = VAL
#       RETURN
#       END
# ''')

# parse('''      PROGRAM MAIN
#       REAL RESULT, CALC         
#       COMMON /SHARE/ A, B        
#       A = 5.0                  
#       B = 10.0
#       RESULT = CALC()         
#       END
#       REAL FUNCTION CALC()       
#       COMMON /SHARE/ A, B      
#       CALC = A + B               
#       RETURN
#       END''')