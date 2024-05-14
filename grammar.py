import lark
import os
from AST import *

class QuackTransformer(lark.Transformer):
    def program(self, data):
        programNode = ProgramNode(data)
        print(programNode.children)
        return programNode
    def r_exp(self, data):
        print(f"r_exp node {data}")
    def sum(self, data):
        print(f"add node {data}")
        buffer = []
        buffer.append(data[0])
        buffer.append(data[1])
        buffer.append("call Int:plus")
        addNode = AddNode(data)
        addNode.buffer = buffer
        return addNode
    def number(self, data):
        #"Convert the value of `tok` from string to int, while maintaining line number & column."
        print(f"number node {data}")
        return "const " + " " + data[0]


directory = "./test_progs"
success = '\x1b[6;30;42m' + 'Success!' + '\x1b[0m'
fail = '\x1b[0;30;41m' + 'FAIL!' + '\x1b[0m'

def main():
    gram_file = open("grammar.lark", "r")
    parser = lark.Lark(gram_file)
    src_file = open("./test_progs/r_exp_test.qk", "r")
    src_text = "".join(src_file.readlines())
    parse_tree = parser.parse(src_text)

    print(parse_tree.pretty())

    transformer = QuackTransformer()
    ast = transformer.transform(parse_tree)
    print(ast)
    print(f"as {repr(ast)}")

def prog_checker():
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