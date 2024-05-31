from lark import Transformer, v_args
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
    
    def while_statement(self, condition, block):
        return While_Node(condition, block)

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