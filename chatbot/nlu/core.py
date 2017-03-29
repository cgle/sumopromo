class Engine(object):
    
    name = None

    def __init__(self, intent_manager=None):
        self.intent_manager = intent_manager

    @classmethod
    def load(cls):
        pass

    def save(self):
        pass

    def train(self):
        raise NotImplementedError
        
    def process(self):
        raise NotImplementedError
        
