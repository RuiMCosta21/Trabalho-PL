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

reserved = ("program", "real", "stop", "end")
tokens = ("INT", "REAL", "DOUBLE", "COMPLEX", "LOGICAL", "CHARACTER", "PARAMETER", "ADD", "SUB", "MULT", "DIV", "EXPO", "VARIABLE")
literals = ("=", "(", ")", ",", ".", "'", "\"",
            "$", "!", ":", "%", "&", "?", "\\", "<", ">")

t_ADD = r"+"
t_SUB = r"\-"
t_EXPO = r"\*\*"
t_MULT = r"\*"
t_DIV = r"\/"

t_INT = r"(-)?\d+"
t_REAL = r"(-)?\d+\.(\d+([eE])?(-)?\d+)?"
t_DOUBLE = r"(-)?\d+\.\d+([dD])?(-)?(\d+)?"
t_COMPLEX = r"\((((-)?\d+)|((-)?\d+\.(\d+([eE])?(-)?\d+)?)), (((-)?\d+)|((-)?\d+\.(\d+([eE])?(-)?\d+)?))\)"
t_LOGICAL = r"\.TRUE\.|\.FALSE\."
t_CHARACTER = r"'['^]'"
t_VARIABLE = r"[a-zA-Z][a-zA-Z0-9]{1,5}"

