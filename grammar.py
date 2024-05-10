from lark import Lark, ast_utils, Transformer, v_args
import os
from AST import *

quack = Lark (r"""
    %import common.WS
    %import common.CNAME -> NAME
    %import common.NUMBER
    
    ident: NAME
    
    program : r_exp
    
    ?r_exp : sum ";"

    ?sum: product
            | sum "+" product   -> add
            | sum "-" product   -> sub
    
        ?product: atom
            | product "*" atom  -> mul
            | product "/" atom  -> div
    
        ?atom: NUMBER           -> number
             | "-" atom         -> neg
             | NAME             -> var
             | "(" sum ")"

    %ignore WS

""", start = "program")

class QuackTransformer(Transformer):
    def program(self, tok):
        print(f"toks are {tok}")
        programNode = ProgramNode(tok)
        print(f"childs are {programNode.children}")
        programNode.walk
    def add(self, tok):
        print(f"add node {tok}")
        left, right = tok
        return left + ".PLUS(" + right + ")"
    def number(self, tok):
        #"Convert the value of `tok` from string to int, while maintaining line number & column."
        ret = "number node"
        print(ret, tok)
        return "const " + " " + tok[0]


directory = "./test_progs"
success = '\x1b[6;30;42m' + 'Success!' + '\x1b[0m'
fail = '\x1b[0;30;41m' + 'FAIL!' + '\x1b[0m'

def main():
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        test_summary = []
        if os.path.isfile(file):
            text = open(file).read()
            try:
                tree = quack.parse(text)
                res_print = tree.pretty()
                print(res_print)
                parse = f"Prog {file} parse......" + success 
                print(parse)
                transform = f"Prog {file} transform......" + success 
                print(transform)
                ans = QuackTransformer().transform(tree)
                print(f"Quack Transform return answer is {ans}")
            except Exception as e:
                exception = ("Exception for file %s......" + fail) % file
                print(exception)
                print(e)
                test_summary.append(exception)
                continue

if __name__=="__main__": 
    main()