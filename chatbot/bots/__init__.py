import logging
from tornado import ioloop, gen

class Bot(object):
    
    name = None

    def __init__(self, manager):
        logging.debug('Setting up {} bot'.format(self.name))
        self.ioloop = ioloop.IOLoop.instance()
        self.manager = manager        

    @property
    def http_client(self):
        return self.manager.http_client
    
    def fetch(self, request):
        return self.http_client.fetch(request)

    def start(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def handle_incoming_data(self, data):
        raise NotImplementedError    

class BotManager(object):
    
    def __init__(self, application=None):
        self.application = application
    
    def register_app(self, application):
        if not self.application:
            self.application = application

    def register_bot(self, bot):
        if not hasattr(self, bot.name):
            setattr(self, bot.name, bot)

    @property
    def http_client(self):
        return self.application.http_client

    @gen.coroutine
    def generate_reply(self, text):
        reply = yield self.application.intent_manager.reply(text)
        return reply

def setup_bots(application):
    from chatbot.bots.facebook import FacebookBot

    manager = BotManager(application=application)
    manager.register_bot(FacebookBot(manager))

    return manager    
