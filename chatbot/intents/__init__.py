import re
from tornado import ioloop, gen

from chatbot.services.facebook import msg as facebook_msg

class Reply(object):   

    def to_facebook(self):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

class TextReply(object):
    
    def __init__(self, text=None):
        self.text = text or ''

    def to_dict(self):
        return {'data': {'text': self.text}}

    def to_facebook(self):
        return facebook_msg.Message(text=self.text)

class Intent(object):

    name = None

    def __init__(self, manager):
        self.manager = manager    
    
    def process(self, *args, **kwargs):
        raise NotImplementedError

    def fetch(self, request):
        return self.manager.http_client.fetch(request)

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
    
    @property
    def http_client(self):
        return self.application.http_client

    @gen.coroutine
    def reply(self, text):
        #TODO USE NLP HERE TO FIND THE CORRECT INTENT

        text = text.lower()
        
        regex = lambda l: re.compile('|'.join([re.escape(x) for x in l]))

        search_regex = regex(['deal', 'promo', 'coupon', 'find', 'search', 'place', 'restaurant'])
        greet_regex = regex(['hi','hey','ola','hello','sup','whatsup'])

        search_match = search_regex.search(text, re.IGNORECASE)
        greet_match = greet_regex.search(text, re.IGNORECASE)

        if search_match:
            intent = self.get_intent('search')
            text = text.replace(search_match.group(0),'').strip()
        elif greet_match:
            intent = self.get_intent('greet')
        else:
            intent = self.get_intent('other')

        replies = yield intent.process(text)

        return replies

def setup_intents(application):

    from chatbot.intents.greet import GreetIntent
    from chatbot.intents.affirm import AffirmIntent
    from chatbot.intents.suggest import SuggestIntent
    from chatbot.intents.search import SearchIntent
    from chatbot.intents.other import OtherIntent

    manager = IntentManager(application=application)
   
    manager.register_intent(GreetIntent(manager))
    manager.register_intent(AffirmIntent(manager))
    manager.register_intent(SuggestIntent(manager))    
    manager.register_intent(SearchIntent(manager))    
    manager.register_intent(OtherIntent(manager))
    
    return manager
