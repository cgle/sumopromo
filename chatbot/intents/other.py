from tornado import gen

from chatbot.intents import TextReply, Intent

class OtherIntent(Intent):
    
    name = 'other'
    
    def __init__(self, *args, **kwargs):
        super(OtherIntent, self).__init__(*args, **kwargs)

    @gen.coroutine
    def process(self):
        return [TextReply(text='Sorry, we are not able to understand your message :( Please try again!')]
