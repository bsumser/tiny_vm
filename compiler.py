from lark import Lark, Transformer, v_args
from AST import *
from QuackChecker import *
from QuackTransformer import *
import sys
import traceback

    
success = '\x1b[6;30;42m' + 'Success!' + '\x1b[0m'
working = '\x1b[1;33;43m' + 'Working...' + '\x1b[0m'
fail = '\x1b[0;30;41m' + 'FAIL!' + '\x1b[0m'

def main():
    # open our grammar file
    gram_file = open_grammar_file()

    # parse file into grammar with lark
    parser = parse_grammar(gram_file)

    # read the input program
    test_prog = read_input_program()

    # construct the parse tree for test program
    parse_tree = parse_code(parser, test_prog)

    # parse the code
    ast = transform_code(parse_tree)

    # typecheck the code
    type_check(ast)
    
    # print graph of concrete syntax tree
    grapher(ast)
    
    # generate code from concrete syntax tree
    generate_code(ast)

    sys.exit(0)
    

def open_grammar_file():
    print("opening grammar file............", end ="..")
    try:
        gram_file = open("./grammar.lark", "r")
        print(f"...............{success}")
        return gram_file
    except Exception as e:
        print(f"opening grammar file...........{fail}")
        print(traceback.format_exc())
        sys.exit(f"Grammar file read exception of {e}")

def parse_grammar(gram_file):
    print("parsing grammar file............", end ="..")
    try:
        parser = Lark(gram_file, parser="lalr")
        print(f"...............{success}")
        return parser
    except Exception as e:
        print(f"parsing grammar file...........{fail}")
        print(traceback.format_exc())
        sys.exit(f"Parsing exception of {e}")

def read_input_program():
    print("reading input program............", end ="..")
    try:
        test_prog = sys.argv[1]
        # read the input program
        src_file = open(test_prog, "r")
        src_text = "".join(src_file.readlines())
        print(f"...............{success}")
        return src_text
    except Exception as e:
        print(f"reading input program...........{fail}")
        print(traceback.format_exc())
        sys.exit(f"Reading input program exception of {e}")

def type_check(ast):
    print(f"type checking program............{working}")
    try:
        # init our typechecker class with our concrete syntax tree
        type_checker = QuackChecker(ast)

        #collect all variable inits
        type_checker.collect_inits()

        print(type_checker.var_inits)

        type_checker.explicit_types()
        if not type_checker.check:
            print(f"type checking program...........{fail}")
            sys.exit("QuackChecker error")
        else:
            print(f"type checking program...................{success}")
    except Exception as e:
        print(f"type checking program...........{fail}")
        print(traceback.format_exc())
        sys.exit(f"QuackChecker type exception: {e}")

def transform_code(parse_tree):
    print(f"transforming ast.................{working}")
    try:
        # initialize our transformer
        transformer = QuackTransformer()
    
        # apply our transformer to the parse tree
        ast = transformer.transform(parse_tree)
        print(f"...............{success}")
        return ast
    except Exception as e:
        print(f"ast transformation..............{fail}")
        print(traceback.format_exc())
        sys.exit(f"Transformer exception: {e}")

def parse_code(parser, test_prog):
    print("parsing input program...............", end ="..")
    try:
        # construct the parse tree for test program
        parse_tree = parser.parse(test_prog)
        print(f"...............{success}")
    
        # print parse tree
        print(parse_tree.pretty())

        return parse_tree

    except Exception as e:
        print(f"...........{fail}")
        print(traceback.format_exc())
        sys.exit(f"exception of {e}")


def generate_code(ast):
    print("generating code for program...............", end ="..")
    try:
        program = ast.code_gen()
        
        with open('QkAsm/qkmain.asm', 'w') as f:
            for line in program:
                # check for none, outputing alternating None
                # values for some reason
                if line != "None":
                    f.write(f"{line}\n")
        print(f"...............{success}")
        print(f"saved to QkAsm/qkmain.asm")
    except Exception as e:
        print(f"...........{fail}")
        print(traceback.format_exc())
        sys.exit(f"exception of {e}")

def grapher(ast):
    print("generating graph............", end ="..")
    try:
        graph = ast.to_graphviz()
        #graph.render('ast', format='png', view=True)
        print(f"...............{success}")
    except Exception as e:
        print(f"...........{fail}")
        print(traceback.format_exc())
        sys.exit(f"exception of {e}")

if __name__=="__main__": 
    main()