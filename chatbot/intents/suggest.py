from chatbot.intents import Intent

class SuggestIntent(Intent):
    
    name = 'suggest'
    
    def __init__(self, *args, **kwargs):
        super(SuggestIntent, self).__init__(*args, **kwargs)

