from chatbot.intents import Intent

class SearchIntent(Intent):
    
    name = 'greeting'
    
    def __init__(self, *args, **kwargs):
        super(SearchIntent, self).__init__(*args, **kwargs)
