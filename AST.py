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