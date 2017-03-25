import logging
from tornado import ioloop, gen

class Service(object):
    
    name = None

    def __init__(self, manager):
        logging.debug('Setting up {} service'.format(self.name))
        self.ioloop = ioloop.IOLoop.instance()
        self.manager = manager
    
    def fetch(self, request):
        return self.manager.http_client.fetch(request)

    def start(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def handle_incoming_data(self, data):
        raise NotImplementedError
        
class ServiceManager(object):
    
    def __init__(self, app):
        self.application = app

    def register_service(self, service):
        if not hasattr(self, service.name):
            setattr(self, service.name, service)
    
    @property
    def http_client(self):
        return self.application.http_client

    @gen.coroutine
    def generate_reply(self, text):
        reply = yield self.application.intent_manager.reply(text)
        return reply

def setup_services(app):
    from chatbot.services.facebook import FacebookService

    manager = ServiceManager(app)
    manager.register_service(FacebookService(manager))

    return manager
