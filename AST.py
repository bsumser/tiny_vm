import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class ASTNode:
    def __init__(self, data):
        print(f"init ASTNode of class {self.__class__.__name__}")
        self.children = data
        print(f"{self.children}")
    
    def walk(self):
        for child in self.children:
            log.debug(f"visit ASTNode of class {child.__class__.__name__}")
            try:
                child.walk()
            except Exception as e:
                log.error(f"fail walk {self.__class__.__name__} to {child.__class__.__name__}")

    def plus(self, e):
        log.debug("-> plus")
        left, right = e
        return left + right
    
    def r_eval(self, buffer: list[str]):
        print("not implemented")

class ProgramNode(ASTNode):
    pass


class AddNode(ASTNode):
    def __init__(self, data):
        print(f"init ASTNode of class {self.__class__.__name__}")
        self.children = data
        print(f"{self.children}")
        self.buffer = []

class Number(ASTNode):
    pass