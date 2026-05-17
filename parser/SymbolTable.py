# A variable cannot belong to more than one common block.
# The variables in a common block do not need to have the same names each place they occur
# (although it is a good idea to do so), but they must be listed in the same order and have the same type and size. 


from .SemanticError import SemanticError

class SymbolTable:
    def __init__(self):
        # { iden: {"kind": ..., "type": ..., "index": ..., "initialized": ...} }
        self.__call_stack = []
        self.__label_count = 0

        self.push()  # global frame

    # -------------------------
    # Call stack management
    # -------------------------

    def push(self):
        self.__call_stack.append({})

    def pop(self):
        if not self.__call_stack:
            raise SemanticError("Call stack underflow")
        self.__call_stack.pop()

    def current_frame(self):
        return self.__call_stack[-1]
    
    def get_tableSize(self):
        return self.__label_count
    
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
            "index": self.__label_count,
            "initialized": False
        }
        self.new_label()

    def declare_array(self, id, tpe, size):
        frame = self.current_frame()
        idx = self.__label_count
        if id in frame:
            raise SemanticError(f"Duplicate declaration: {id}")

        frame[id] = {
            "kind": "array",
            "type": tpe,
            "index": idx,
            "initialized": False,
            "size": size
        }
        self.update_label(size)

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
    
    # guarantees unique identifier for labels
    def new_label(self):
        self.__label_count += 1
        return self.__label_count
    
    def update_label(self, size):
        self.__label_count += size

    # -------------------------
    # Debug
    # -------------------------

    def dump(self):
        print("\n=== SYMBOL TABLE DUMP ===")

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
                        f"value={entry['index']} init={entry['initialized']}"
                    )
                elif entry["type"] == "Label":
                    print(
                        f"  LABEL {name:10}"
                    )
                elif entry["type"] == "array":
                    print(
                        f"  VAR {name:10} type={entry['type']} "
                        f"value={entry['index']} init={entry['initialized']}"
                        f"size={entry['size']}"
                    )
                elif entry["kind"] == "fun":
                    print(
                        f"  FUN {name:10} type={entry['type']} "
                        f"params={entry.get('params')}"
                    )
                else:
                    print(f"  ??? {name:10} {entry}")

        print("\n=== END DUMP ===\n")