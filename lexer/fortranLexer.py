import ply.lex as lex

# Program organization
      #program name

      #declarations

      #statements

      #stop
      #end

# Column position rules

# Fortran 77 is not a free-format language, 
# but has a very strict set of rules for how the source code should be formatted. 
# The most important rules are the column position rules:

#   Col. 1    : Blank, or a "c" or "*" for comments
#   Col. 1-5  : Statement label (optional)
#   Col. 6    : Continuation of previous line (optional)
#   Col. 7-72 : Statements
#   Col. 73-80: Sequence number (optional, rarely used today)

# Most lines in a Fortran 77 program starts with 6 blanks and ends before column 72, i.e. only the statement field is used.
 
# Any character can be used instead of the plus sign as a continuation character. 
# It is considered good programming style to use either the plus sign, an ampersand,
# or digits (using 2 for the second line, 3 for the third, and so on). 

class LexError(Exception):
    pass

states = (('startLine', 'exclusive'),
          ('formatState', 'inclusive'),)

reserved = ("program", "stop", "end",
            "if", "then", "else", "elseif", "endif",
            "do", "continue", "enddo", "while", "goto", "until",
            "dimension",
            "function", "return",
            "subroutine", "call",
            "common",
            "block",
            "print", "read", "write", 
            "mod", "cos", "sen",
            "format")

tokens = ("PROGRAM", "NAME", "STOP", "END",
          "INT_IDEN", "REAL_IDEN", "DOUBLE_IDEN", "COMPLEX_IDEN", "LOGICAL_IDEN", "CHARACTER_IDEN",
          "IF", "THEN", "ELSE", "ELSEIF", "ENDIF",
          "DO", "CONTINUE", "ENDDO", "WHILE", "GOTO", "UNTIL", "DO_WHILE",
          "DIMENSION",
          "FUNCTION", "RETURN",
          "SUBROUTINE", "CALL",
          "COMMON", "SEPARATOR",
          "DATA", "BLOCK",
          "PRINT", "READ", "WRITE",
          "MOD", "COS", "SEN",
          "FORMAT", "FORMAT_CODE",
          "INT", "REAL", "DOUBLE", "COMPLEX", "LOGICAL", "CHARACTER",
          "PARAMETER", "IDEN",
          "ADD", "SUB", "MULT", "DIV", "EXPO",
          "LESSTHAN", "LESSEQ", "GREATERTHAN", "GREATEREQ", "EQ", "NOTEQ",
          "AND", "OR", "NOT",
          "LABEL",
          "comment")

literals = ("=", "(", ")", ",", "\"", "+", "-", "*",
            "$", "!", ":", "%", "&", "?", "\\", "<", ">")

def t_PROGRAM(t):
    r"PROGRAM|program"
    t.lexer.name_flag = True
    return t

t_STOP = r"STOP|stop"
t_END = r"END|end"

def t_INT_IDEN(t):
    r"INTEGER|integer"
    return t

def t_REAL_IDEN(t):
    r"REAL|real"
    return t

def t_DOUBLE_IDEN(t):
    r"DOUBLE PRECISION|double precision"
    return t

def t_COMPLEX_IDEN(t):
    r"COMPLEX|complex"
    return t

def t_LOGICAL_IDEN(t):
    r"LOGICAL|logical" 
    return t

def t_CHARACTER_IDEN(t):
    r"CHARACTER|character"
    return t

def t_IF(t):
    r"IF|if"
    return t

def t_THEN(t):
    r"THEN|then"
    return t

t_ELSE = r"ELSE|else"
t_ELSEIF = r"ELSEIF|elseif"
t_ENDIF = r"ENDIF|endif"


def t_DO(t):
    r"DO|do"
    t.lexer.do_label_flag = True
    return t

def t_CONTINUE(t):
    r"CONTINUE|continue"
    return t

t_ENDDO = r"ENDDO|enddo"

def t_WHILE(t):
    r"WHILE|while"
    t.lexer.do_label_flag = False
    return t

def t_GOTO(t):
    r"GOTO|goto"
    t.lexer.do_label_flag = True
    return t

t_UNTIL = r"UNTIL|until"

def t_DIMENSION(t):
    r"DIMENSION|dimension"
    return t

def t_FUNCTION(t):
    r"FUNCTION|function"
    t.lexer.name_flag = True
    return t

t_RETURN = r"RETURN|return"

def t_SUBROUTINE(t):
    r"SUBROUTINE|subroutine"
    t.lexer.name_flag = True
    return t

t_CALL = r"CALL|call"

def t_COMMON(t):
    r"COMMON|common"
    t.lexer.separator_flag = True
    return t

def t_DATA(t):
    r"DATA|data"
    if t.lexer.separator_flag == True:
        t.type = "IDEN"
    else: 
        t.lexer.separator_flag = True
    return t

t_BLOCK = r"BLOCK|block"

def t_FORMAT(t):
    r"FORMAT|format"
    t.lexer.begin('formatState')
    return t

def t_formatState_FORMAT_CODE(t):
    r"(\d+)?[ADEFIXadefix](\d+(\.\d+)?)?|/"
    t.type = 'FORMAT_CODE'
    return t

def t_formatState_RPAREN(t):
    r"\)"
    t.type = ')'
    t.lexer.begin('INITIAL') 
    return t

t_EXPO = r"\*\*"


def t_DIV(t):
    r"\/"
    if t.lexer.separator_flag == True:
        t.type = "SEPARATOR"
    return t

def t_COMPLEX(t):
    r"\((([+-]?\d+)|[+-]?(\d+\.\d*|\d*\.\d+)([eE][+-]?\d+)?), (([+-]?\d+)|[+-]?(\d+\.\d*|\d*\.\d+)([eE][+-]?\d+)?)\)"
    return t 

def t_REAL(t):
    r"[+-]?(\d+\.\d*|\d*\.\d+)([eE][+-]?\d+)?" # retirado da aula teórica
    return t

def t_DOUBLE(t):
    r"[+-]?(\d+\.\d*|\d*\.\d+)([dD][+-]?\d+)?"
    return t

def t_INT(t):
    r"(-)?\d+"
    if t.lexer.do_label_flag == True:
        t.type = "LABEL"
        t.lexer.do_label_flag = False
    t.value = int(t.value)
    return t


t_LOGICAL = r"\.TRUE\.|\.FALSE\."

def t_CHARACTER(t):
    r"'[^']*'"
    return t

def t_IDEN(t):
    r"[a-zA-Z]([a-zA-Z0-9]*)?|[a-zA-Z]([a-zA-Z0-9]{1,5})?"
    if t.lexer.name_flag == True:
        t.type = "NAME"
        t.lexer.name_flag = False
    else:
        # Check if the word is reserved
        val = t.value.lower()
        if val in reserved:
            t.type = val.upper()
    return t

t_PARAMETER = r"parameter"

t_LESSTHAN = r"\.LT\."
t_LESSEQ = r"\.LE\."
t_GREATERTHAN = r"\.GT\."
t_GREATEREQ = r"\.GE\."
t_EQ = r"\.EQ\."
t_NOTEQ = r"\.NE\."
t_AND = r"\.AND\."
t_OR = r"\.OR\."
t_NOT = r"\.NOT\."

t_ignore = " \t"

def t_ANY_newline(t):
    r"(\n+)"
    t.lexer.lineno += len(t.value)
    t.lexer.line_start = t.lexer.lexpos
    t.lexer.previous_state = t.lexer.lexstate
    t.lexer.begin('startLine')
    t.lexer.separator_flag = False
    t.lexer.name_flag = False

def t_startLine_comment(t):
    r"[cC*].*"

def t_startLine_MARGIN(t):
    r'[0-9 ]{5}.'
    col6 = t.value[5]
    
    if col6 not in (' ', '0'):
        t.lexer.begin(t.lexer.previous_state)
    else:
        t.lexer.begin('INITIAL')

    label_part = t.value[:5].strip()
    if label_part:
        t.type = 'LABEL'
        t.value = int(label_part)
        return t

def t_error(t):
  raise LexError(f"Invalid symbol: {t.value[0]}")

t_startLine_ignore ="\t"

def t_startLine_error(t):
  raise LexError(f"Invalid symbol: {t.value[0]}")

fortranLexer = lex.lex()

