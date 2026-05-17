class CodeGenerator:
    def __init__(self, symbols):
        self.symbols = symbols

    def gen_print(self, items):
        code = []

        for v in items:
            # STRING LITERAL
            if isinstance(v, str) and v.startswith("'") and v.endswith("'"):
                v = f'"{v[1:-1]}"'
                code.append(f"PUSHS {v}")
                code.append("WRITES")
                continue

            # VARIABLE
            var_info = self.symbols.lookup(v)

            code.append(f"PUSHG {var_info['index']}")

            var_type = var_info["type"]

            if var_type == "INTEGER":
                code.append("WRITEI")
            elif var_type == "REAL":
                code.append("WRITEF")
            elif var_type == "CHARACTER":
                code.append("WRITES")
            else:
                raise Exception(f"Unknown type: {var_type}")

        return code
    
    def gen_read(self, variables):
        code = []
        code +=[f"// Read begins"]
        for v in variables:
            if isinstance(v, tuple):
                name, indexes = v
                info = self.symbols.lookup(name)
                
                code += [f"PUSHFP",
                         f"PUSHI {info['index']}",
                         f"PADD"]

                idx = indexes[0]
                if isinstance(idx, int):
                    code += [f"PUSHI {idx}"]
                else:
                    idx_info = self.symbols.lookup(idx)
                    code += [f"PUSHG {idx_info['index']}"]
                code += [
                    "PUSHI 1",
                    "SUB",
                ]

                code += ["READ"]
                if info["type"] == "INTEGER":
                    code += ["ATOI"]
                elif info["type"] == "REAL":
                    code += ["ATOF"]

                code += ["STOREN"]

            else:
                info = self.symbols.lookup(v)

                code += ["READ"]

                if info["type"] == "INTEGER":
                    code += ["ATOI"]
                elif info["type"] == "REAL":
                    code += ["ATOF"]

                code += [f"STOREG {info['index']}"]

        return code
    
    def gen_loop(self, loop_var, start, end, step, body):
        #       DO 10      I   =   1,    N  , (step)
        start_label = f"LOOPSTART{loop_var}"
        end_label = f"LOOPEND{loop_var}"
        var_info = self.symbols.lookup(loop_var)
        self.symbols.initialize(loop_var)

        code = [f"//Início do loop"]

        code += [
            f"{start[0]}",
            f"STOREG {var_info['index']}"
        ]
        code += [f"{start_label}:"]

        code += [
            f"PUSHG {var_info['index']}",
            f"{end[0]}",
            "INFEQ",
            f"JZ {end_label}"
        ]
        code +=[f"// Body"]
        code += body

        code += [f"// I = I + step"]
        code += [f"PUSHG {var_info['index']}"]
        code += step
        code += ["ADD"]
        code += [f"STOREG {var_info['index']}"]

        code += [
            f"JUMP {start_label}",
            f"{end_label}:"
        ]

        return code
    
    def gen_factor(self, factor):
        code = []

        if isinstance(factor, int):
            code = [f"PUSHI {factor}"]
        elif isinstance(factor, float):
            code = [f"PUSHF {factor}"]
        elif isinstance(factor, list):
            code = factor
        else:
            var_info = self.symbols.lookup(factor)
            code = [f"PUSHG {var_info['index']}"]

        return code
    
    def gen_array_access(self, array, access_index):
        code = []
        code +=[f"// Accessing array"]
        info = self.symbols.lookup(array)
        base = info['index']

        code += [f"PUSHFP",
                 f"PUSHI {base}",
                 f"PADD"]

        # index (can be variable or constant or expression)
        code += access_index

        code.append("PUSHI 1")
        code.append("SUB")

        code.append("LOADN")

        return code
    
    def gen_mod(self, arguments):
        code = []
        for v in arguments:
            if(isinstance(v, int)):
                code += [f"PUSHI {v}"]
                continue

            var_info = self.symbols.lookup(v)
            code += [f"PUSHG {var_info['index']}"]
        
        code += [f"MOD"]
        return code

    def gen_boolean(self, argument):
        code = []
        val = 1 if argument == '.TRUE.' else 0
    
        code += [f"PUSHI {val}"]
        return code
    
    def gen_cond_expression(self, left_expr, op, right_expr):
        code = []
        code += [f"//Starting condition expression"]
        code += left_expr 
        code += right_expr

        # vm não tem "NOTEQ"
        if op == "NOTEQ":
            code += ["EQUAL", "NOT"]
        else:
            code += op

        return code
    
    def gen_condition(self, left_side, op_inst, right_side):
        code = []
        code += [f"//Starting condition"]
        code += left_side
        code += right_side 
        code += op_inst
        return code
    
    def gen_GOTO(self, label, line_number):
    
        # Log the reference silently
        self.symbols.reference_label(label, line_number)

        # Instantly emit the text target instruction
        code = [f"JUMP L{label}"]
        return code

    def gen_if_statement(self, code_conditions, then_body, else_body=None):
            if_id = self.symbols.new_label()

            # Define internal jump targets
            else_label = f"IEELSE{if_id}"
            end_label = f"IEEND{if_id}"

            code = []
            code += [f"//Starting if Statement"]
            code += code_conditions

            # If condition is 0 (False), jump to ELSE (or END if no else)
            if else_body:
                code += [f"JZ {else_label}"]
            else:
                code += [f"JZ {end_label}"]

            code += [f"//Then body"]
            code += then_body

            if else_body:
                code += [f"JUMP {end_label}"]

                code += [f"{else_label}:"]
                code += else_body

            code += [f"{end_label}:"]

            code +=[f"//Finishing if statement"]
            return code
                


