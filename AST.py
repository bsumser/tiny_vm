import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class ASTNode:
    def __init__(self, data):
        log.debug(f"init ASTNode of class {self.__class__.__name__}")
        self.children = data
        log.debug(f"{self.children}")
    
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