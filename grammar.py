from lark import Lark
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

directory = "./test_progs"
success = '\x1b[6;30;42m' + 'Success!' + '\x1b[0m'
fail = '\x1b[0;30;41m' + 'FAIL!' + '\x1b[0m'

for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    if os.path.isfile(file):
        text = open(file).read()
        try:
            res = quack.parse(text).pretty()
            #print(res)
            print(f"Prog {file} passed......" + success)
        except Exception as e:
            print(("Exception for file %s......" + fail) % file)
            print(e)
            continue
