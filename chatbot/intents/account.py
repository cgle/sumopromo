from tornado import gen

from chatbot.intents import TextReply, Intent

class AccountIntent(Intent):
    
    name = 'account'
    
    def __init__(self, *args, **kwargs):
        super(AccountIntent, self).__init__(*args, **kwargs)

    @gen.coroutine
    def process(self):
        return [TextReply(text='View or change your account settings here (y)')]

