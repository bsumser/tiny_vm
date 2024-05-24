from lark import Lark, Transformer, v_args
from AST import *


@v_args(inline=True)
class QuackTransformer(Transformer):
    def program(self, *statements):
        return ProgramNode(statements)

    def assignment(self, var_type, var_name, value):
        return AssigNode(var_type, var_name, value)
    
    def add(self, left, right):
        return OpHelp(left, right, '+')

    def sub(self, left, right):
        return OpHelp(left, right, '-')

    def mul(self, left, right):
        return OpHelp(left, right, '*')

    def div(self, left, right):
        return OpHelp(left, right, '/')

    def number(self, value):
        return NumberNode(int(value))

    def ident(self, name):
        return IdentNode(name)

    def neg(self, value):
        return OpHelp(NumberNode(0), value, '-')  # Unary minus can be treated as 0 - value
    
    def r_exp(self, expression):
        return R_ExpNode(expression)
    
    @v_args(inline=False)
    def if_statement(self, data):
        return If_Node(data)
    
    @v_args(inline=False)
    def else_statement(self, data):
        return Else_Node(data)

    def log_exp(self, left, right):
        return Log_Exp_Node(left, right)
    
    def return_statement(self, value):
        return Return_Node(value)

    def equals(self, left, right):
        return Equals_Node(left, right)

    def less_equals(self, left, right):
        return Temp_Node(left, right)

    def less_than(self, left, right):
        return Less_Than_Node(left, right)

    def great_equals(self, left, right):
        return Temp_Node(left, right)

    def great_than(self, left, right):
        return Temp_Node(left, right)

    def and_(self, left, right):
        return Temp_Node(left, right)

    def or_(self, left, right):
        return Temp_Node(left, right)

    def not_(self, left, right):
        return Temp_Node(left, right)


def main():
    gram_file = open("grammar.lark", "r")
    parser = Lark(gram_file)
    src_file = open("./test_progs/r_exp_test.qk", "r")
    src_text = "".join(src_file.readlines())
    parse_tree = parser.parse(src_text)

    print(parse_tree.pretty())

    transformer = QuackTransformer()
    ast = transformer.transform(parse_tree)
    print(f"ast is {repr(ast)}")
    print(repr(ast.walk()))
    graph = ast.to_graphviz()
    graph.render('ast', format='png', view=True)
    program = ast.code_gen()

    for line in program:
        print(line)

    with open('out.asm', 'w') as f:
        for line in program:
            f.write(f"{line}\n")

if __name__=="__main__": 
    main()