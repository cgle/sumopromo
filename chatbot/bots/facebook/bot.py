import logging

from tornado import gen

from chatbot.bots import Bot
from chatbot.bots.facebook import msg

class FacebookBot(Bot):
        
    name = 'facebook'

    def __init__(self, *args, **kwargs):
        super(FacebookBot, self).__init__(*args, **kwargs)
        self._ready = True

    @property
    def ready(self):
        return self._ready

    @gen.coroutine
    def start(self):
        bot_settings = [msg.SettingRequest(setting_type='domain_whitelisting', 
                                           whitelisted_domains=['https://www.sumopromo.com'], 
                                           domain_action_type='add'),
                        msg.SettingRequest(setting_type='greeting', 
                                           greeting={'text': 'SumoPromo - A real-time, location-based, on-demand promotion platform.'}),]

        yield [self.fetch(setting.to_http_request()) for setting in bot_settings]
        self._ready = True
    
    @gen.coroutine
    def handle_incoming_data(self, data):
        logging.debug('Facebook bot handling incoming data ', data)
        if not self.ready:
            logging.error('Facebook bot is not ready yet')
            return

        message_requests = []
        message_events = data['entry'][0]['messaging']
        for event in message_events:
            try:
                request = yield self.generate_message_request(event)
                message_requests.append(request)
            except KeyError:
                continue
        
        logging.debug('Facebook bot sending replies to client')
        try:
            yield [ self.fetch(request.to_http_request()) for request in message_requests ]
        except Exception as e:
            logging.error(e)

        return
        
    
    @gen.coroutine    
    def generate_message_request(self, event):
        text = event['message']['text']
        sender_id = event['sender']['id']

        recipient = msg.Recipient(recipient_id=sender_id)
        
        reply = yield self.manager.generate_reply(text)

        message_request = msg.MessageRequest(recipient, reply.to_facebook())
        return message_request
