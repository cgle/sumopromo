import random

from tornado import gen

import chatbot.services.facebook.msg as facebook_msg
from chatbot.intents import Reply, Intent
from chatbot.misc.router import url_for

class GreetReply(Reply):

    __slots__ = ('text',)

    name = 'greet'
    texts = [
        'Hey there, welcome to SumoPromo :D!',
        'Howdy! Welcome to SumoPromo :D!',
        'Ola! We would love to find you some nice deals <3!',
        'Welcome back <3!',
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

class LinkAccountReply(Reply):

    def to_facebook(self):
        login_button = facebook_msg.AccountLinkButton(url_for('account.facebook_auth'))
        template = facebook_msg.ButtonTemplate('Please log in!', [login_button])
        attachment = facebook_msg.TemplateAttachment(template)
        message = facebook_msg.Message(attachment=attachment)
        return message

class FBLoginReply(Reply):

    def to_facebook(self):
        login_button = facebook_msg.WebUrlButton('Log In', url_for('account.facebook_auth'))
        template = facebook_msg.ButtonTemplate('Please log in!', [login_button])
        attachment = facebook_msg.TemplateAttachment(template)
        message = facebook_msg.Message(attachment=attachment)
        return message

class GreetIntent(Intent):
    
    name = 'greet'

    def __init__(self, *args, **kwargs):
        super(GreetIntent, self).__init__(*args, **kwargs)
        
    @gen.coroutine
    def process(self):
        return [GreetReply(), FBLoginReply()]
