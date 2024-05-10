import logging

class ASTNode:
    def __init__(self):
        log = logging.getLogger(__name__)
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
        log.debug(f"init astNode")
        self.children = []
    
    def walk(self):
        for child in flatten(self.children):
            log.debug(f"visit ASTNode of class {child.__class__.__name__}")

            try:
                child.walk()
            except Exception as e:
                log.error(f"fail walk {self.__class__.__name__} to {child.__class__.__name__}")

    def plus(self, e):
        log.debug("-> plus")
        left, right = e
        return left + right