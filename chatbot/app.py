import logging

from tornado import web, gen, httpclient
from concurrent.futures import ThreadPoolExecutor

from chatbot.handlers import init_handlers
from chatbot.bots import setup_bots
from chatbot.intents import setup_intents

from chatbot.config import config

httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')

class ChatbotApp(web.Application):

    executor = None

    def __init__(self, custom_config=None):
        self.config = custom_config or config

        super(ChatbotApp, self).__init__(init_handlers(), **self.config.app)
        
        # set up reusable attrs
        self.executor = ThreadPoolExecutor(max_workers=config.MAX_THREADS)
        self.http_client = httpclient.AsyncHTTPClient()
        
        logging.debug('Setting up bots in app')
        self.bot_manager = setup_bots(self)

        logging.debug('Setting up intents in app')        
        self.intent_manager = setup_intents(self)
