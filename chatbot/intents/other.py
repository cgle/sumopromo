from chatbot.intents import Intent

class OtherIntent(Intent):
    
    name = 'other'
    
    def __init__(self, *args, **kwargs):
        super(OtherIntent, self).__init__(*args, **kwargs)

