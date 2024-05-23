from lark import Lark, Transformer, v_args
from AST import *
import collections


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