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

    statement : assignment
              | r_exp

    assignment : ident "=" int ";"
              | ident "=" r_exp ";"
    r_exp : int
              | r_exp "+" r_exp ";"
              | r_exp "-" r_exp ";"
              | r_exp "*" r_exp ";"
              | r_exp "/" r_exp ";"
              | "-" r_exp ";"
    %ignore WS

""", start = "program")

directory = "./test_progs"

for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    if os.path.isfile(file):
        text = open(file).read()
        try:
            res = quack.parse(text).pretty()
            print(res)
            print(f"Prog {file} passed")
        except:
            print("Exception occured for file %s" % file)
            continue