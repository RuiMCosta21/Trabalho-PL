# A variable cannot belong to more than one common block.
# The variables in a common block do not need to have the same names each place they occur
# (although it is a good idea to do so), but they must be listed in the same order and have the same type and size. 


from .SemanticError import SemanticError

class SymbolTable:
    def __init__(self):
        # { iden: {"kind": ..., "type": ..., "index": ..., "initialized": ...} }
        self.__call_stack = []
        self.__index_count = 0
        self.__internal_label_count = 0 # internal labels for flow control, independent from frame
        self.__label_stack = [] # List of dicts: [{"defined": {}, "referenced": {}}]

        self.push()  # global frame

    # -------------------------
    # Call stack management
    # -------------------------

    def push(self):
        self.__call_stack.append({})
        self.__label_stack.append({
            "defined": {},
            "referenced": {}
        })

    def pop(self):
        """Closes the current scope and validates all labels inside it."""
        if len(self.__label_stack) <= 1:
            raise Exception("Cannot pop global scope.")
            
        # Validate this frame before destroying it
        self.validate_current_frame_labels()
        
        self.__call_stack.pop()
        self.__label_stack.pop()

    def current_frame(self):
        return self.__call_stack[-1]
    
    def current_label_frame(self):
        return self.__label_stack[-1]
    
    def get_tableSize(self):
        return self.__index_count
    
     # return all declared symbols
    def symbols(self, kind=None):
        scope = self.current_frame()
        if kind is None:
            return scope.items()
        return [
            (name, entry)
            for name, entry in scope.items()
            if entry["kind"] == kind
        ]

    # -------------------------
    # Lookup
    # -------------------------

    def lookup(self, id):
        for frame in reversed(self.__call_stack):
            if id in frame:
                entry = frame[id]
                if entry["kind"] not in ("var", "array", "fun"):
                    raise SemanticError(f"Identifier is not a variable: {id}")
                return entry
        raise SemanticError(f"Undeclared variable: {id}")
    
    def lookup_label(self, id):
        for frame in reversed(self.__label_stack):
            if id in frame:
                entry = frame[id]
                return entry
        raise SemanticError(f"Undeclared label: {id}")

    # -------------------------
    # Declarations
    # -------------------------

    def declare_var(self, id, tpe):
        frame = self.current_frame()

        if id in frame:
            raise SemanticError(f"Duplicate declaration: {id}")

        frame[id] = {
            "kind": "var",
            "type": tpe,
            "index": self.__index_count,
            "initialized": False
        }
        self.new_index()

    def declare_array(self, id, tpe, size):
        frame = self.current_frame()
        idx = self.__index_count
        if id in frame:
            raise SemanticError(f"Duplicate declaration: {id}")

        frame[id] = {
            "kind": "array",
            "type": tpe,
            "index": idx,
            "initialized": False,
            "size": size
        }
        self.update_index(size)

    def declare_label(self, label_iden, target_statement):
        """Called when a label is physically encountered (e.g., '20 IF...')"""
        current_frame = self.__label_stack[-1]
        
        if label_iden in current_frame["defined"]:
            raise Exception(f"Label {label_iden} already defined in this scope.")
            
        current_frame["defined"][label_iden] = {
            "index": label_iden,
            "target": target_statement
        }
        return target_statement
    
    def reference_label(self, label_iden, line_no):
        """Called when a GOTO encounters a label. We just note it down for later."""
        current_frame = self.__label_stack[-1]
        
        # Log that this label was used, and remember where it happened for error reporting
        if label_iden not in current_frame["referenced"]:
            current_frame["referenced"][label_iden] = line_no

    def validate_current_frame_labels(self):
        """Checks if any label was referenced but never physically defined."""
        current_frame = self.__label_stack[-1]
        
        for label_iden, line_no in current_frame["referenced"].items():
            if label_iden not in current_frame["defined"]:
                # The compiler pass is finishing this block, and the label never showed up!
                raise Exception(f"Semantic Error at line {line_no}: Undeclared label: {label_iden}")

    def declare_fun(self, id, tpe, params):
        # Search for the ID in the global/current scope
        frame = self.current_frame()

        if id in frame:
            entry = frame[id]

            # Check if this was just a type declaration from an INTEGER/REAL statement
            if entry.get("kind") == "var" and entry.get("type") == tpe:
                # Upgrade the existing entry to a function
                entry["kind"] = "fun"
                entry["params"] = params
                entry["initialized"] = True 
                return
            else:
                # If it's already a function or a conflicting type, then error out
                raise SemanticError(f"Duplicate function declaration: {id}")

        # If not found at all, create it from scratch
        frame[id] = {
            "kind": "function",
            "type": tpe,
            "params": params,
            "initialized": True
        }

    def initialize(self, id):
            # it's a tuple if initializing an array (Iden, size)
            base_id = id[0] if isinstance(id, tuple) else id

            for frame in reversed(self.__call_stack):
                if base_id in frame:
                    entry = frame[base_id]
                    if entry["kind"] in ("var", "array"):
                        entry["initialized"] = True
                        return

            raise SemanticError(f"Undeclared variable or array: {base_id}")
    
    # guarantees unique identifier for indexes
    def new_index(self):
        self.__index_count += 1
        return self.__index_count
    
    def update_index(self, size):
        self.__index_count += size
    
    def new_label(self):
        self.__internal_label_count += 1
        return self.__internal_label_count
    # -------------------------
    # Debug
    # -------------------------

    def dump(self):
        print("\n=== SYMBOL TABLE DUMP ===")

        # ----------------------------------------------------
        # 1. PRINT CALL STACK (VARIABLES & FUNCTIONS)
        # ----------------------------------------------------
        print("\n--- Call Stack ---")
        for i, frame in enumerate(reversed(self.__call_stack)):
            level = len(self.__call_stack) - 1 - i
            print(f"\nFrame {level}:")

            if not frame:
                print("  (empty)")
                continue

            for name, entry in frame.items():
                if entry["kind"] == "var" and entry["type"] != "Label":
                    print(
                        f"  VAR {name:10} type={entry['type']} "
                        f"index={entry['index']} init={entry['initialized']}"
                    )
                elif entry["type"] == "array":
                    print(
                        f"  ARRAY {name:8} type={entry['type']} "
                        f"index={entry['index']} init={entry['initialized']} "
                        f"size={entry.get('size', 1)}"
                    )
                elif entry["kind"] == "fun":
                    print(
                        f"  FUN {name:10} type={entry['type']} "
                        f"params={entry.get('params')}"
                    )
                else:
                    print(f"  ??? {name:10} {entry}")

        # ----------------------------------------------------
        # 2. PRINT LABEL STACK (DEFINED VS REFERENCED)
        # ----------------------------------------------------
        print("\n--- User-Defined Label Stack ---")
        for i, label_frame in enumerate(reversed(self.__label_stack)):
            level = len(self.__label_stack) - 1 - i
            print(f"\nFrame {level} Labels:")

            defined_labels = label_frame.get("defined", {})
            referenced_labels = label_frame.get("referenced", {})

            if not defined_labels and not referenced_labels:
                print("  (no labels defined or referenced in this scope)")
                continue

            # Show labels that have a physical destination line/statement
            if defined_labels:
                print("  [Defined Placement Targets]")
                for label_id, entry in defined_labels.items():
                    target_info = f" target={entry.get('target')}" if entry.get('target') is not None else ""
                    print(
                        f"    LABEL {label_id:8} index={entry.get('index', label_id)}{target_info}"
                    )

            # Show labels that are currently anticipated by an active GOTO line
            if referenced_labels:
                print("  [Referenced GOTO Requests]")
                for label_id, line_no in referenced_labels.items():
                    print(
                        f"    LABEL {label_id:8} targeted at line {line_no}"
                    )

        # ----------------------------------------------------
        # 3. PRINT GLOBAL METADATA Counters
        # ----------------------------------------------------
        print("\n--- Global State Metadata ---")
        # Safely read private count field using getattr in case naming convention changes
        internal_count = getattr(self, "_SymbolTable__internal_label_count", 0)
        print(f"Total Internal Flow Control Labels Generated: {internal_count}")

        print("\n=== END DUMP ===\n")