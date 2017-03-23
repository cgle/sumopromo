from tornado import ioloop, gen

class Reply(object):
    
    name = None

    def to_facebook(self):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

class Intent(object):

    name = None

    def __init__(self, manager):
        self.manager = manager    
    
    def process(self, *args, **kwargs):
        raise NotImplementedError

class IntentManager(object):
    
    def __init__(self, application=None):
        self.application = application        
        self.io_loop = ioloop.IOLoop.instance()

        self._intents = {}

    @property
    def intents(self):
        return self._intents

    def get_intent(self, name):
        try:
            return self._intents[name]
        except KeyError:
            return None

    def register_app(self, application):
        if not self.application:
            self.application = application

    def register_intent(self, intent):
        if intent.name not in self._intents:
            self._intents[intent.name] = intent
    
    @gen.coroutine
    def reply(self, text):
        #TODO USE NLP HERE TO FIND THE CORRECT INTENT
        intent = self.get_intent('greeting')
        return intent.process()

def setup_intents(application):
    from chatbot.intents.greeting import GreetingIntent
    from chatbot.intents.search import SearchIntent
    from chatbot.intents.other import OtherIntent

    manager = IntentManager(application=application)
   
    manager.register_intent(GreetingIntent(manager))
    manager.register_intent(SearchIntent(manager))
    manager.register_intent(OtherIntent(manager))
    
    return manager
