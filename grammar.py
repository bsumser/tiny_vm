from lark import Lark, Transformer
import os

quack = Lark (r"""
    %import common.WS
    %import common.CNAME
    %import common.NUMBER
    
    literal: int
    int: NUMBER 
    ident: CNAME
    
    program : class* statement*
    
    class : ident ";"

    statement : assignment ";"
              | r_exp ";"
              | l_exp ";"
              | return_statement ";"

    assignment : l_exp ":" ident "=" r_exp

    l_exp : ident
            | r_exp "." ident ";"

    r_exp : int
              | r_exp "+" r_exp
              | r_exp "-" r_exp
              | r_exp "*" r_exp
              | r_exp "/" r_exp
              | "-" r_exp

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
    def INT(self, tok):
        "Convert the value of `tok` from string to int, while maintaining line number & column."
        return tok.update(value=int(tok))


directory = "./test_progs"
success = '\x1b[6;30;42m' + 'Success!' + '\x1b[0m'
fail = '\x1b[0;30;41m' + 'FAIL!' + '\x1b[0m'

for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    if os.path.isfile(file):
        text = open(file).read()
        try:
            tree = quack.parse(text)
            res_print = tree.pretty()
            print(res_print)
            print(f"Prog {file} parse......" + success)
            print(f"Prog {file} transform......" + success)
            QuackTransformer().transform(tree)
        except Exception as e:
            print(("Exception for file %s......" + fail) % file)
            print(e)
            continue
