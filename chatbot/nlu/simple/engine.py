import logging
import re
from leven import levenshtein as lvsn
from functools import partial
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

from chatbot.nlu.core import Engine

regex = lambda l: re.compile('|'.join([re.escape(x) for x in l]), re.I)

# TODO: USE SPACY TO CLEAN UP TEXT AND TOKENIZE
class SimpleNLU(Engine):
    
    SEARCH_WORDS = ['deal', 'promo', 'coupon', 'find', 'search', 'place', 'get', 'want', 'give']
    GREET_WORDS = ['hi','hey','ola','hello','sup', 'whats up']

    search_regex = regex(SEARCH_WORDS)
    greet_regex = regex(GREET_WORDS)

    def __init__(self, *args, **kwargs):
        super(SimpleNLU, self).__init__(*args, **kwargs)

    def process(self, text):
        text = self.clean_up(text)
        #func = self.get_intent_function_regex(text)
        func = self.get_intent_function_lvsn(text)
        
        try:
            replies = func()
            return replies
        except Exception as e:
            logging.error('SimpleNLU cannot process {}: {}'.format(text, e))
            return []

    def clean_up(self, text):
        text = re.sub(' +', ' ', text.strip()).lower()
        text = ' '.join([word for word in text.split() if word not in ENGLISH_STOP_WORDS])
        return text

    def get_intent_function_regex(self, text):
        func = None

        # use regex
        search_match = self.search_regex.search(text)
        greet_match = self.greet_regex.search(text)
        
        if search_match:
            intent = self.intent_manager.get('search')
            func = partial(intent.process, query=text.replace(search_match.group(0).strip(), ''))
        elif greet_match:
            func = self.intent_manager.get('greet').process
        else:
            func = self.intent_manager.get('other').process

        return func

    def get_intent_function_lvsn(self, text):
        logging.debug('INPUT TEXT {}'.format(text))
        func = None
                
        # simple nlp matching algorithm functions
        lvsn_score = lambda t,l: sum([ ( lvsn(t,w) ) for w in l ])
        normalized_text_score = lambda t,l: lvsn_score(t,l) / len(''.join(l))
        normalized_word_score = lambda t,l: lvsn_score(t,l) / len(t)

        # score of texts with keywords
        text_scores = [ ('search', normalized_text_score(text, self.SEARCH_WORDS)),
                        ('greet',  normalized_text_score(text, self.GREET_WORDS)) ]

        name, score = min(text_scores, key=lambda x:x[1])
        
        if name == 'search':
            intent = self.intent_manager.get('search')

            word_scores = [ (normalized_word_score(word, self.SEARCH_WORDS), word) for word in text.split() ]

            _, query = max(word_scores, key=lambda x:x[0])

            func = partial(intent.process, query=query)
            
            logging.debug('SEARCHING {}'.format(query))

        elif name == 'greet':
            func = self.intent_manager.get('greet').process
        else:
            func = self.intent_manager.get('other').process

        return func
