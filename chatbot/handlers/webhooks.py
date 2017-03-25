import ujson, logging
from tornado import web, gen

from chatbot.config import config

class FacebookWebhookHandler(web.RequestHandler):

    @property
    def bot(self):
        return self.application.services.facebook

    @web.asynchronous
    def get(self):
        verify_token = self.get_argument('hub.verify_token', default=None)
        hub_challenge = self.get_argument('hub.challenge', default=None)
        if verify_token == config.social['facebook']['verify_token']:
            self.write(hub_challenge)
        else:
            self.set_status(500)
            self.write('Invalid verify_token')
        self.finish()
        return
    
    @gen.coroutine
    def post(self):
        data = ujson.loads(self.request.body)
        logging.debug('Dispatching message to FB Bot')
        self.bot.handle_incoming_data(data)
        self.write('OK')
        self.finish()
        return

handlers = [
    (r'/webhooks/facebook', FacebookWebhookHandler),
]
