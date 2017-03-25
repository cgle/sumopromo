from chatbot.intents import Intent

class AffirmIntent(Intent):
    
    name = 'affirm'
    
    def __init__(self, *args, **kwargs):
        super(AffirmIntent, self).__init__(*args, **kwargs)

