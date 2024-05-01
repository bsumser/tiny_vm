from lark import Lark, Transformer
import os

quack = Lark (r"""
    %import common.WS
    %import common.CNAME -> NAME
    %import common.NUMBER
    
    ident: NAME
    
    program : statement
    
    class : ident ";"

    statement : assignment ";"
        | r_exp ";"
        | l_exp ";"
        | return_statement ";"

    assignment : l_exp ":" ident "=" r_exp

    ?l_exp : ident
            | r_exp "." ident ";"

    ?r_exp : NUMBER
            | sum
            | r_exp sum r_exp

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

    return_statement: "return" r_exp
                        | "return" l_exp
    %ignore WS

""", start = "program")

class QuackTransformer(Transformer):
    def program(self, ret = "program node"):
        print(ret)
    def statement(self, ret = "statement node"):
        print(ret)
    def r_exp(self, ret = "r_exp node"):
        print(ret)
    def add(self, ret = "r_exp node"):
        print(ret)
    def NUMBER(self, tok):
        "Convert the value of `tok` from string to int, while maintaining line number & column."
        return tok.update(value=int(tok))


directory = "./test_progs"
success = '\x1b[6;30;42m' + 'Success!' + '\x1b[0m'
fail = '\x1b[0;30;41m' + 'FAIL!' + '\x1b[0m'

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
            transform = f"Prog {file} transform......" + success 
            print(parse)
            print(transform)
            test_summary.append(parse)
            test_summary.append(transform)
            QuackTransformer().transform(tree)
        except Exception as e:
            exception = ("Exception for file %s......" + fail) % file
            print(exception)
            print(e)
            test_summary.append(exception)
            continue
    for res in test_summary:
        print(res)
