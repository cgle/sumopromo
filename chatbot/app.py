from tornado import web, gen, httpclient
from concurrent.futures import ThreadPoolExecutor

from chatbot.server import config
from chatbot.handlers import init_handlers

httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')

class ChatbotApp(web.Application):

    executor = ThreadPoolExecutor(max_workers=config.MAX_THREADS)

    def __init__(self, settings):
        super(ChatbotApp, self).__init__(init_handlers(), **settings)

        self.http_client = httpclient.AsyncHTTPClient()
