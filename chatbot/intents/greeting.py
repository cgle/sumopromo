import random

import chatbot.bots.facebook.msg as facebook_msg
from chatbot.intents import Reply, Intent

class GreetingReply(Reply):
    __slots__ = ('text',)
    name = 'greeting'
    texts = [
        'Hey there, welcome to SumoPromo :D!',
        'Howdy! Welcome to SumoPromo :D!',
        'Ola! We would love to find you some nice deals :D!',
        'Welcome back!',
    ]

    def __init__(self, text=None):
        self.text = text or random.choice(self.texts)

    def to_dict(self):
        return {
            'name': self.name, 
            'data': {'text': self.text}
        }

    def to_facebook(self):
        return facebook_msg.Message(text=self.text)

class GreetingIntent(Intent):
    
    name = 'greeting'

    def __init__(self, *args, **kwargs):
        super(GreetingIntent, self).__init__(*args, **kwargs)

    def process(self):
        return GreetingReply()
