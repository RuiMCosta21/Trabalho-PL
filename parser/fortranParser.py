from . import SymbolTable
from .SemanticError import SemanticError

from lexer.fortranLexer import tokens
import ply.yacc as yacc

def p_program(p):
    r"""
    Program : PROGRAM NAME Lines END Program_continuations
    """
    size = p.parser.symbols.get_tableSize()
    alloc = ["PUSHI 0" for _ in range(size)]
    p[0] = alloc + p[3]

def p_program_continuations(p):
    r"""
    Program_continuations : Program_continuations Program_continuation
                         | 
    """       
    
def p_program_continuation(p):
    r"""
    Program_continuation : Type Fun NAME '(' Arguments ')' Lines RETURN END
    """
    p.parser.symbols.pop()
    p.parser.symbols.declare_fun(p[3], p[1], p[5])    

def p_fun_aux(p):
    r"""
    Fun : FUNCTION
    """
    p.parser.symbols.push()            

def p_lines(p):
    r"""
    Lines : Lines Line
          | Line
    """
    if len(p) == 2:
      p[0] = p[1]
    else:
      p[0] = p[1] + p[2]
    
def p_line(p):
    r"""
    Line : Start Statement
    """
    print(p[1], p[2])
    if p[1] is not None:
        p.parser.symbols.declare_label(p[1], p[2])
        p[0] = [f"L{p[1]}:"] + p[2]
    else:
        p[0] = p[2]
    
def p_start(p):
    r"""
    Start : LABEL
          | 
    """
    if len(p) > 1:
        p[0] = p[1]
    
def p_statement(p):
    # incompleto
    r"""
    Statement : FuncCall
              | Declaration
              | Assignment
              | Do_Statement
              | If_Statement
              | Goto_statement
    """
    p[0] = p[1]

##################### Variable Declaration ##################################
def p_declaration(p):
    r"""
    Declaration : Type Variables
                | COMMON SEPARATOR IDEN SEPARATOR Variables
    """
    var_list = p[2]
    for var in var_list:
        if isinstance(var, tuple):
            iden, size = var
            p.parser.symbols.declare_array(iden, p[1], size[0]) # size é uma lista 
        else:
            p.parser.symbols.declare_var(var, p[1])
    p[0] = []
    
def p_type(p):
    r"""
    Type : INT_IDEN
         | REAL_IDEN
         | DOUBLE_IDEN
         | COMPLEX_IDEN
         | LOGICAL_IDEN
         | CHARACTER_IDEN
    """
    p[0] = p[1]

def p_variables_multiple(p):
    r"Variables : Variables ',' Variable"
    p[0] = p[1] + [p[3]]

def p_variables_single(p):
    r"Variables : Variable"
    p[0] = [p[1]]

def p_variable(p):
    r"""
    Variable : Array
             | CHARACTER
             | IDEN
    """
    p[0] = p[1]

def p_array(p):
    r"""
    Array : IDEN '(' Indexes ')'"""
    p[0] = (p[1], p[3])

def p_indexes_multiple(p):
    r"""
    Indexes : Indexes ',' Index
    """
    p[0] = p[1] + [p[3]]

def p_indexes_single(p):
    r"""
    Indexes : Index
    """
    p[0] = [p[1]]

def p_index(p):
    r"""
    Index : INT
          | IDEN
    """
    p[0] = p[1]

##################### Predefined Function Calls ###################################
def p_funcCall(p):
    r"""
    FuncCall : IO_Function
             | Math_Function 
    """
    p[0] = p[1]

def p_Standard_Math_Function(p):
    r"""
    Math_Function : MOD '(' Variables ')'
    """
    if(len(p[3]) > 2):
        raise ParseError(f"Invalid number of arguments. MOD expects 2 arguments")
    p[0] = p.parser.codegen.gen_mod(p[3])
        
def p_Standard_Function(p):
    r"""
    IO_Function : WRITE Def Variables
    """
    p[0] = p[1]

def p_Standard_Function_print(p):
    r"""
    IO_Function : PRINT Def Variables
    """
    p[0] = p.parser.codegen.gen_print(p[3])

def p_Standard_Function_read(p):
    r"""
    IO_Function : READ Def Variables
    """
    p.parser.symbols.initialize(p[3][0])
    p[0] = p.parser.codegen.gen_read(p[3])

def p_def(p):
    r"""
    Def : '(' UnitNo ',' LABEL ')'
        | UnitNo ','
    """
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = p[2] + p[4]

def p_unitno(p):
    r"""
    UnitNo : INT
           | '*'
    """
    p[0] = p[1]

########################### Assignments ##########################################
def p_assignment(p):
    r"""
    Assignment : IDEN '=' Expression_paren
    """
    var_info = p.parser.symbols.lookup(p[1])
    p.parser.symbols.initialize(p[1])
    # produce the value of the expression, and store it in the current frame
    p[0] = p[3] + [f"STOREL {var_info['index']}"]

def p_expression_paren(p):
    r"""
    Expression_paren : '(' Expression ')'
                     | Expression
    """
    if len(p) > 2 :
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_expression_e(p):
    r"""
    Expression : E
               | LOGICAL 
    """
    if p.slice[1].type == 'LOGICAL':
        p[0] = p.parser.codegen.gen_boolean(p[1])
    else:
        p[0] = p[1]

def p_function(p):
    r"""
    Function : IDEN '(' Arguments ')'
    """
def p_function_arguments(p):
    r"""
    Arguments : Arguments ',' Argument
    """
    p[0] = p[1] + [p[3]]

def p_function_arguments_single(p):
    r"""
    Arguments : Argument
    """
    p[0] = [p[1]]

def p_Argument(p):
    r"""
    Argument : Variable
             | 
    """
    if len(p) > 1:
        p[0] = p[1]

################ Expressões aritméticas ########################
def p_expr_sum(p):
    r"""
    E : E '+' T
    """
    p[0] = p[1] + p[3] + [f"ADD"]

def p_expr_sub(p):
    r"""
    E  : E "-" T
    """
    p[0] = p[1] + p[3] + [f"SUB"]

def p_expr_term(p):
    r"""
    E  : T
    """
    p[0] = p[1]

def p_term_expo(p):
    r"""
    T : T EXPO F
    """
def p_term_mul(p):
    r"""
    T  : T "*" F
    """
    p[0] = p[1] + p[3] + [f"MUL"] 

def p_term_div(p):
    r"""
    T  : T DIV F
    """
    p[0] = p[1] + p[3] + [f"DIV"]

def p_term_factor(p):
    r"""
    T  : F
    """
    p[0] = p[1]


###################### Factor #############################
def p_factor(p):
    r"""
    F  : '(' E ')'
       | Math_Function
       | IDEN Suffix
       | INT
       | REAL
       | DOUBLE
       | COMPLEX
    """
    result = []
    symbol_type = p.slice[1].type
    if symbol_type in ('INT', 'REAL', 'DOUBLE', 'COMPLEX'):
        result = p.parser.codegen.gen_factor(p[1])
    elif symbol_type == 'Math_Function':
        result = p[1] 

    elif len(p) == 4:
        result = p[2]
    else:
        info = p.parser.symbols.lookup(p[1])

        if info["kind"] == "array":
            result = (p.parser.codegen.gen_array_access(p[1], p.parser.codegen.gen_factor(p[2][0])))
        elif info["kind"] == "fun":
            result = (
                "function_call",
                p[1],
                p[2]
            )
        elif info["kind"] == "var":
            result = p.parser.codegen.gen_factor(p[1])
        else:
            raise SemanticError(f"{p[1]} is not callable/indexable") 
    p[0] = result

def p_reference(p):
    r"""
    Suffix : '(' Arguments ')'
           | 
    """
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = []


#################### DO blocks ############################
def p_do_statement(p):
    r"""
    Do_Statement : DO LABEL IDEN '=' Loop_Values Lines LABEL CONTINUE
    """
    if p[2] != p[7]:
        raise SemanticError(f"DO label mismatch: {p[2]} vs {p[7]}")
    
    p[0] = p.parser.codegen.gen_loop(p[3], *p[5], p[6])
    
    
def p_Loop_Values(p):
    r"""
    Loop_Values : Loop_Value ',' Loop_Value
                | Loop_Value ',' Loop_Value ',' Loop_Value
    """
    if len(p) == 4:
        # Matches: Start ',' End
        p[0] = (p[1], p[3], p.parser.codegen.gen_factor(1))
    else:
        # Matches: Start ',' End ',' Step
        p[0] = (p[1], p[3], p[5])
    

def p_Loop_Value(p):
    r"""
    Loop_Value : INT
               | REAL
               | IDEN
    """
    p[0] = p.parser.codegen.gen_factor(p[1])

################### If Statements #########################
def p_if_statement(p):
    r"""
    If_Statement : IF '(' Conditions ')' THEN Lines If_Continuation ENDIF
    """
    p[0] = p.parser.codegen.gen_if_statement(p[3], p[6], p[7])

def p_conditions(p):
    r"""
    Conditions : Conditions BoolOp Condition
    """
    p[0] = p.parser.codegen.gen_condition(p[1], p[2], p[3])

def p_conditions_single(p):
    r"""
    Conditions : Condition
    """
    p[0] = p[1]

def p_boolOp(p):
    r"""
    BoolOp : AND
    """
    p[0] = [f"AND"]

def p_boolOp_or(p):
    r"""
    BoolOp : OR
    """
    p[0] = [f"OR"]

def p_condition(p):
    r"""
    Condition : Expression_paren CondOp Expression_paren
    """
    p[0] = p.parser.codegen.gen_cond_expression(p[1], p[2], p[3])

def p_condition_single(p):
    r"""
    Condition : Expression_paren
    """
    p[0] = p[1]

def p_condOp_lessthan(p):
    r"""
    CondOp : LESSTHAN
    """
    p[0] = [f"INF"] 

def p_condOp_lesseq(p):
    r"""
    CondOp : LESSEQ
    """
    p[0] = [f"INFEQ"] 

def p_condOp_greaterthan(p):
    r"""
    CondOp : GREATERTHAN
    """
    p[0] = [f"SUP"]  

def p_condOp_greatereq(p):
    r"""
    CondOp : GREATEREQ
    """
    p[0] = [f"SUPEQ"]  

def p_condOp_eq(p):
    r"""
    CondOp : EQ
    """
    p[0] = [f"EQUAL"]  

def p_condOp_noteq(p):
    r"""
    CondOp : NOTEQ
    """
    p[0] = [f"NOTEQ"]  

def p_if_continuation(p):
    r"""
    If_Continuation : ELSE Lines 
                    | 
    """
    if len(p) > 2:
        p[0] = p[2]

def p_goto(p):
    r"""
    Goto_statement : GOTO LABEL
    """
    line_number = p.lineno(2)
    p[0] = p.parser.codegen.gen_GOTO(p[2], line_number)

class ParseError(Exception):
    pass

def p_error(t):
    raise ParseError(f"Unexpected token: {t.type if t else '$'}") # ply assumes None at end of input

fortranParser = yacc.yacc()
