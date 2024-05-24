import logging
from graphviz import Digraph

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class ASTNode:
    def __init__(self):
        self.children = []
        print(f"init ASTNode of class {self.__class__.__name__}")

    def walk(self):
        for child in self.children:
            child.walk()

    def __repr__(self):
        return repr(self.__dict__)

    def code_gen(self):
        raise NotImplemented("AST BASE CLASS")

    def to_graphviz(self, graph=None, parent_id=None):
        if graph is None:
            graph = Digraph()

        node_id = str(id(self))
        label = self.__class__.__name__
        if isinstance(self, OpHelp):
            label += f' ({self.op})'
        elif isinstance(self, NumberNode):
            label += f' ({self.value})'
        elif isinstance(self, IdentNode):
            label += f' ({self.name})'

        graph.node(node_id, label)

        if parent_id is not None:
            graph.edge(parent_id, node_id)

        for child in self.children:
            print(type(child))
            child.to_graphviz(graph, node_id)

        return graph

                

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements
        self.children = statements

    def code_gen(self):
        buffer = []
        code = (f"code gen at {self.__class__.__name__}")
        print(code)
        for child in self.children:
            child.code_gen(buffer)
        return buffer

class AssigNode(ASTNode):
    def __init__(self, var_type, var_name, value):
        self.var_type = var_type
        self.var_name = var_name
        self.value = value
        self.children = [var_name, var_type, value]
    
    def code_gen(self, buffer):
        code = (f"code gen at {self.__class__.__name__}")
        print(code)
        self.value.code_gen(buffer)
        self.var_type.code_gen(buffer)
        return True

class OpHelp(ASTNode):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op
        self.children = [left, right]

    def code_gen(self, buffer):
        code = (f"code gen at {self.__class__.__name__}")
        print(code)
        opDict = {
          "+": "Int:plus",
          "-": "Int:minus",
          "/": "Int:divi",
          "*": "Int:multi",
        }

        for child in self.children:
            child.code_gen(buffer)
        buffer.append(f"call {opDict[self.op]}")
        return True
    
    def walk(self):
        print(self.children)

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
        self.children = value

    def walk(self):
        print(self.value)

    def code_gen(self, buffer):
        code = (f"code gen at {self.__class__.__name__}")
        print(code)
        buffer.append(f"const {self.value}")
        return True
    
    def to_graphviz(self, graph=None, parent_id=None):
        if graph is None:
            graph = Digraph()

        node_id = str(id(self))
        label = self.__class__.__name__
        graph.node(node_id, label)

        if parent_id is not None:
            graph.edge(parent_id, node_id)

        return graph

class IdentNode(ASTNode):
    def __init__(self, name):
        self.name = name
        self.children = name
    
    def walk(self):
        print(self.name)
    
    def code_gen(self, buffer):
        code = (f"code gen at {self.__class__.__name__}")
        print(code)
        buffer.insert(0, f".local {self.name}")
        buffer.append(f"store {self.name}")
        return True

    
    def to_graphviz(self, graph=None, parent_id=None):
        if graph is None:
            graph = Digraph()

        node_id = str(id(self))
        label = self.__class__.__name__
        graph.node(node_id, label)

        if parent_id is not None:
            graph.edge(parent_id, node_id)

        return graph

class R_ExpNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression
        self.children = [expression]

    def code_gen(self, buffer):
        code = (f"code gen at {self.__class__.__name__}")
        print(code)
        for child in self.children:
            child.code_gen(buffer)
        return True
    
class If_Node(ASTNode):
    def __init__(self, data):
        print(f"if node data: {data}")
        self.condition = data[0]
        self.if_block = data[1]
        self.label_count = 0
        self.else_if_blocks = data[2:-1] if len(data) > 3 else []
        self.else_block = data[-1] if len(data) > 2 else None
        self.children = data

    def code_gen(self, buffer):
        code = (f"code gen at {self.__class__.__name__}")
        print(f"if node data: {self.children}")
        print(code)

        # generate all of the needed labels
        last_label = self.label_gen()
        else_if_labels = [self.label_gen() for _ in self.else_if_blocks]
        else_label = self.label_gen() if self.else_block else last_label
        
        # visit the children
        self.condition.code_gen(buffer)
        buffer.append(f"jump_ifnot {else_if_labels[0] if self.else_if_blocks else else_label}")
        self.if_block.code_gen(buffer)
        buffer.append(f"jump {last_label}")

        # visit else if
        for num in range(0, len(self.else_if_blocks), 2):
            buffer.append(f"{else_if_labels[num]}:")
            self.else_if_blocks[num].code_gen(buffer)
            buffer.append(f"jump_ifnot {else_if_labels[num+1] if (num + 1) < len(self.else_if_blocks) else else_label}")
            self.else_if_blocks[num].code_gen(buffer)
            buffer.append(f"jump {last_label}")

        # visit else

        # end label
        buffer.append(last_label+":")

    def label_gen(self):
        label = f"label{self.label_count}"
        self.label_count += 1
        return label
        

class Log_Exp_Node(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.children = [left, right]

class Less_Than_Node(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.children = [left, right]

    def code_gen(self, buffer):
        code = (f"code gen at {self.__class__.__name__}")
        print(code)
        buffer.append(code)
        self.left.code_gen(buffer)
        self.right.code_gen(buffer)

class Equals_Node(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.children = [left, right]

    def code_gen(self, buffer):
        code = (f"code gen at {self.__class__.__name__}")
        print(code)
        self.left.code_gen(buffer)
        self.right.code_gen(buffer)
        buffer.append(f"call Int:Equals")


class Temp_Node(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.children = [left, right]