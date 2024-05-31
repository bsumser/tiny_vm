import sys
import AST

class QuackChecker():
    def __init__(self, ast):
        self.tree = ast
        self.check = True
        self.reserved = ["class", "def", "extends", "if", "elif", 
                         "else", "while", "return", "and", "or", 
                         "not", "typecase"] 

        self.identifiers = ["String", "Int", "Obj", "Boolean", 
                             "true", "false", "Nothing", "none"]

        self.types = ["Int", "Boolean", "Obj"]

        self.var_inits = {}

        #print(f"init typechecker of class {self.__class__.__name__}")
        #print(f"{self.tree.children}")

    def explicit_types(self):
        
        def check_types(root):
            if root.children:
                for node in root.children:
                    check_types(node)
                    print(type(root))
            check_explicit_type(root)


        def check_explicit_type(node):
            if isinstance(node, AST.AssigNode):
                # check to make sure type is supported
                if node.var_type.name not in self.types:
                    raise Exception(f"Unsupported type of {node.var_type.name} found")
                
                # check to make sure name is not reserved keyword
                if node.var_name.name in self.types:
                    raise Exception(f"Usage of reserved keyword {node.var_name.name} as name found")
            
            if isinstance(node, AST.R_ExpNode):
                if node.expression in self.types:
                    raise Exception(f"Usage of reserved keyword {node.expression} as name found")
            
            if isinstance(node, AST.OpHelp):
                # TODO: check if same types
                if type(node.left) is AST.OpHelp:
                    # recurse down
                    print("recurse down")
                    check_explicit_type(node.left)
                elif type(node.left) is not AST.OpHelp and type(node.right) is not AST.OpHelp:
                    print(node.left, node.right)
                    if type(node.left) is not AST.NumberNode:
                        leftType = self.var_inits[node.left.name]
                    else:
                        leftType = node.left.type
                    if type(node.right) is not AST.NumberNode:
                        rightType = self.var_inits[node.right.name]
                    else:
                        rightType = node.right.type

                    if leftType != rightType:
                        print(type(leftType))
                        print(type(rightType))
                        raise Exception(f"Type mismatch of {leftType} to {rightType} on operation {node.op}")

            
            #if isinstance(node, AST.Return_Node):
            #    # check to make sure name is not reserved keyword
            #    if node.value.name in self.types:
            #        raise Exception(f"Usage of reserved keyword {node.value.name} as name found")
    
        check_types(self.tree)

    def collect_inits(self):

        def walk(root):
            if isinstance(root, AST.AssigNode):
                # TODO: fix this, no idea why this works 
                # still has a token in the name and type field for some reason
                self.var_inits[root.var_name.name[0]] = root.var_type.name[0:3]

            if root.children:
                for node in root.children:
                    walk(node)
                    print(type(root))
        walk(self.tree)


    def check_expression_node():
        print(f"checking program node")