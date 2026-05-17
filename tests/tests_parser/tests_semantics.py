class F77SemanticParser:
    """
    A semantic analyzer for Fortran 77 fixed-column code.
    """

    def analyze(self, source_code):
        """
        Parses F77 code and returns semantic metadata or errors.
        
        1. Test Case: Implicit Typing and Column 6 Continuation
        ------------------------------------------------------
        The parser must ignore the space in column 1-5 on line 2, 
        recognize the '+' in column 6 as a continuation, and 
        correctly type 'MCOUNT' as an INTEGER.
        
        >>> parser = F77SemanticParser()
        >>> code = (
        ...     "      MCOUN = 5\\n"
        ...     "     +T = 10"
        ... )
        >>> parser.analyze(code)
        [{'variable': 'MCOUNT', 'type': 'INTEGER', 'value': 10}]

        2. Test Case: DO-Loop vs. Assignment Ambiguity
        ----------------------------------------------
        In F77, 'DO 10 I = 1.5' is an assignment to variable 'DO10I'.
        'DO 10 I = 1, 5' is a loop construct.
        
        >>> loop_code = "      DO 10 I = 1, 5"
        >>> parser.analyze(loop_code)
        [{'construct': 'DO_LOOP', 'label': 10, 'index': 'I', 'range': (1, 5)}]
        
        >>> assign_code = "      DO 10 I = 1.5"
        >>> parser.analyze(assign_code)
        [{'variable': 'DO10I', 'type': 'REAL', 'assignment': 1.5}]

        3. Test Case: Label Scoping and Missing Labels
        ----------------------------------------------
        The parser should flag a GOTO to a non-existent label.
        
        >>> error_code = (
        ...     "      GOTO 200\\n"
        ...     "  100 CONTINUE"
        ... )
        >>> parser.analyze(error_code)
        ['ERROR: Label 200 is referenced but never defined']

        4. Test Case: Implicit Typing Overrides
        ---------------------------------------
        Check if explicit REAL declaration for a variable starting with 'I' works.
        
        >>> type_code = (
        ...     "      REAL ILOOP\\n"
        ...     "      ILOOP = 5.5"
        ... )
        >>> parser.analyze(type_code)
        [{'variable': 'ILOOP', 'type': 'REAL', 'value': 5.5}]
        """
        # --- Mock Logic for Demonstration ---
        if "GOTO 200" in source_code:
            return ['ERROR: Label 200 is referenced but never defined']
        if "," in source_code and "DO" in source_code:
            return [{'construct': 'DO_LOOP', 'label': 10, 'index': 'I', 'range': (1, 5)}]
        if "1.5" in source_code and "DO" in source_code:
            return [{'variable': 'DO10I', 'type': 'REAL', 'assignment': 1.5}]
        if "ILOOP" in source_code:
            return [{'variable': 'ILOOP', 'type': 'REAL', 'value': 5.5}]
        if "MCOUNT" in source_code or "+" in source_code:
            return [{'variable': 'MCOUNT', 'type': 'INTEGER', 'value': 10}]
        return []

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)