import logging

from tornado import gen

from chatbot.services import Service
from chatbot.services.facebook import msg
from chatbot.misc.router import url_for

class FacebookService(Service):
        
    name = 'facebook'

    def __init__(self, *args, **kwargs):
        super(FacebookService, self).__init__(*args, **kwargs)
        self._ready = False
        self.start()

    @property
    def ready(self):
        return self._ready

    @gen.coroutine
    def start(self):
        settings = [msg.SettingRequest(setting_type='domain_whitelisting', 
                                       whitelisted_domains=['https://www.sumopromo.com'], 
                                       domain_action_type='add'),
                    msg.SettingRequest(setting_type='account_linking_url',
                                       account_linking_url=url_for('account.facebook_auth')),
                    msg.SettingRequest(setting_type='greeting', 
                                       greeting=[
                                           {
                                               'text': 'SumoPromo - A real-time, location-based, on-demand promotion platform.',
                                               'locale': 'default'
                                           }
                                       ]),]

        yield [self.fetch(setting.to_http_request()) for setting in settings]
        self._ready = True
    
    @gen.coroutine
    def handle_incoming_data(self, data):
        logging.debug('Facebook service handling incoming data ', data)

        if not self.ready:
            logging.error('Facebook service is not ready yet')
            return

        message_requests = []
        message_events = data['entry'][0]['messaging']
        for event in message_events:
            try:
                requests = yield self.generate_message_requests(event)
                message_requests += requests
            except KeyError:
                continue
        
        logging.debug('Facebook service sending replies to client')
        try:
            for request in message_requests:
                # send one by one, in order
                yield self.fetch(request.to_http_request())
        except Exception as e:
            logging.error(e)
            raise

        return
            
    @gen.coroutine
    def generate_message_requests(self, event):
        text = event['message']['text']
        sender_id = event['sender']['id']

        recipient = msg.Recipient(recipient_id=sender_id)
        
        replies = yield self.manager.generate_replies(text)
        
        requests = [ msg.MessageRequest(recipient, reply.to_facebook()) for reply in replies ]

        return requests
