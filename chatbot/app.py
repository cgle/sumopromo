import logging

from tornado import web, gen, httpclient
from concurrent.futures import ThreadPoolExecutor

from chatbot.handlers import init_handlers

from chatbot.intents import setup_intents
from chatbot.services import setup_services

from chatbot.config import config

httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')

class ChatbotApp(web.Application):

    executor = None

    def __init__(self, custom_config=None, bots=None):
        self.config = custom_config or config

        super(ChatbotApp, self).__init__(init_handlers(), **self.config.app)
        
        # set up reusable attrs
        self.executor = ThreadPoolExecutor(max_workers=config.MAX_THREADS)
        self.http_client = httpclient.AsyncHTTPClient()       

        logging.debug('Setting up services in app')
        self.services = setup_services(self)

        logging.debug('Setting up intents in app')
        self.intent_manager = setup_intents(self)
        
