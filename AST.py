import logging
from graphviz import Digraph
from QuackChecker import *

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

    def code_gen(self, buffer):
        raise NotImplemented("AST BASE CLASS")

    def to_graphviz(self, graph=None, parent_id=None):
        if graph is None:
            graph = Digraph()

        node_id = str(id(self))
        
        # old way to make label
        label = self.__class__.__name__

        if isinstance(self, OpHelp):
            label += f' ({self.op})'
        elif isinstance(self, NumberNode):
            label += f' ({self.value})'
        elif isinstance(self, IdentNode):
            label += f' ({self.name})'
        elif isinstance(self, VarNode):
            label += f' ({self.name})'

        graph.node(node_id, label)

        if parent_id is not None:
            graph.edge(parent_id, node_id)

        for child in self.children:
            print(type(self))
            print(type(child))
            child.to_graphviz(graph, node_id)

        return graph
 
class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements
        self.children = statements


    def code_gen(self):
        buffer = []
        buffer.append(".class $Main:Obj")
        buffer.append(".method $constructor")
        buffer.append(".local ")
        for child in self.children:
            child.code_gen(buffer)
        return buffer

class AssigNode(ASTNode):
    #TODO: need to add support for assig without type identifier

    def __init__(self, data):
        #case for init with ident
        self.var_name = data[0]
        self.var_type = data[1]
        self.value = data[2]
        if data[1] is None:
            del data[1]
        self.children = data
        
        #old stuff
        #self.var_type = var_type
        #self.var_name = var_name
        #self.value = value
        #self.children = [var_type, var_name, value]
    
    def code_gen(self, buffer):
        if (self.var_type == None):
            buffer.append(f"{self.value.code_gen(buffer)}")
            buffer.append(f"store {self.var_name.get_name()}")
        else:
            buffer[2] += f"{self.var_name.get_name()},"
            buffer.append(f"{self.value.code_gen(buffer)}")
            buffer.append(f"store {self.var_name.get_name()}")

class OpHelp(ASTNode):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op
        self.children = [right, left]

    def code_gen(self, buffer):
        opDict = {
          "+": "Int:plus",
          "-": "Int:minus",
          "/": "Int:divi",
          "*": "Int:multi",
        }

        for child in self.children:
            child.code_gen(buffer)
        buffer.append(f"call {opDict[self.op]}")
    
    def walk(self):
        print(self.children)

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
        self.type = "Int"
        self.children = None

    def walk(self):
        print(self.value)

    def code_gen(self, buffer):
        buffer.append(f"const {self.value}")
    
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
        self.children = None
    
    def walk(self):
        print(self.name)
    
    def code_gen(self, buffer):
        # old way, doesnt load right in situations such as x = y + 1
        buffer.append(f"load {self.name}")
    
    def code_gen_init(self, buffer):
        buffer.insert(0,f".local {self.name}")
    
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
        for child in self.children:
            child.code_gen(buffer)
    
class L_ExpNode(ASTNode):
    def __init__(self, name):
        self.name = name
        self.children = [name]

    def code_gen(self, buffer):
        raise Exception(f"{self.__class__.__name__} code gen not implemented")

class VarNode(ASTNode):
    def __init__(self, name):
        self.name = name
        self.children = None
    
    def walk(self):
        print(self.name)
    
    def code_gen(self, buffer):
        buffer.append(f"load {self.name}")
        #raise Exception(f"{self.__class__.__name__} code gen not implemented")
    
    def get_name(self):
        return self.name

    def to_graphviz(self, graph=None, parent_id=None):
        if graph is None:
            graph = Digraph()

        node_id = str(id(self))
        label = self.__class__.__name__
        graph.node(node_id, label)

        if parent_id is not None:
            graph.edge(parent_id, node_id)

        return graph

class If_Node(ASTNode):
    def __init__(self, data):
        print(f"if node data: {data}")
        self.condition = data[0]
        self.block = data[1]
        self.else_block = data[2] if len(data) > 2 else None
        self.children = data
        self.label_count = 0

    def code_gen(self, buffer):
        # make the labels
        last_label = self.label_gen()
        else_label = self.label_gen() if self.else_block else last_label

        #evaluate condition
        self.condition.code_gen(buffer)
        buffer.append(f"jump_ifnot {else_label}")

        #evalute block
        self.block.code_gen(buffer)
        buffer.append(f"jump {last_label}")

        # visit else_block if it exists
        if self.else_block:
            buffer.append(f"{else_label}:")
            label_num = self.label_count
            self.else_block.code_gen(buffer, label_num, last_label)

        # last label
        buffer.append(f"{last_label}:")

    def label_gen(self):
        if ('global_label_count' not in globals()):
            #init the global label counter
            global global_label_count
            global_label_count = 0
        label = f"label{self.label_count}"
        self.label_count += 1 + global_label_count
        global_label_count += 1
        return label
        
class Else_Node(ASTNode):
    def __init__(self, data):
        print(f"else node node data: {data}")
        if len(data) > 1:
            self.condition = data[0]
            self.block = data[1]
            self.else_block = data[2]
        else:
            self.else_block = None
            self.block = data[0]
        self.children = data

    def code_gen(self, buffer, label_num, last_label):
        # pass current label number down to else
        self.label_count = label_num
        
        else_label = self.label_gen() if self.else_block else last_label

        if len(self.children) > 1:
            #evaluate condition
            self.condition.code_gen(buffer)
            buffer.append(f"jump_ifnot {else_label}")

            #evalute block
            self.block.code_gen(buffer)
            buffer.append(f"jump {last_label}")

            # visit else_block if it exists
            if self.else_block:
                buffer.append(f"{else_label}:")
                label_num = self.label_count
                self.else_block.code_gen(buffer, label_num, last_label)

        else:
            #evalute block
            self.block.code_gen(buffer)
            buffer.append(f"jump {last_label}")


    def label_gen(self):
        if ('global_label_count' not in globals()):
            #init the global label counter
            global global_label_count
            global_label_count = 0
        label = f"label{self.label_count}"
        self.label_count += 1 + global_label_count
        global_label_count += 1
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
        self.left.code_gen(buffer)
        self.right.code_gen(buffer)
        buffer.append(f"call Int:equals")

class Equals_Node(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.children = [left, right]

    def code_gen(self, buffer):
        self.left.code_gen(buffer)
        self.right.code_gen(buffer)
        buffer.append(f"call Int:equals")

class Return_Node(ASTNode):
    def __init__(self, value):
        self.value = value
        self.children = [value]

    def code_gen(self, buffer):
       self.value.code_gen(buffer)
       buffer.append(f"return 1") 

class While_Node(ASTNode):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
        self.children = [condition, block]
        self.label_count = 0
    
    def code_gen(self, buffer):
        # make labels for start and end of the loop
        start_label = self.label_gen()
        last_label = self.label_gen()

        buffer.append(f"{start_label}:")

        # evaluate the condition
        self.condition.code_gen(buffer)
        buffer.append(f"jump_ifnot {last_label}")
        self.block.code_gen(buffer)
        buffer.append(f"jump {start_label}")
        buffer.append(f"{last_label}:")
    
    def label_gen(self):
        if ('global_label_count' not in globals()):
            #init the global label counter
            global global_label_count
            global_label_count = 0
        label = f"label_while{self.label_count}"
        self.label_count += 1 + global_label_count
        global_label_count += 1
        return label

class Temp_Node(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.children = [left, right]
