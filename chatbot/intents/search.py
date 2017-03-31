import ujson
from tornado import gen

import chatbot.services.facebook.msg as facebook_msg
from chatbot.intents import Reply, Intent, TextReply

from chatbot.misc.router import url_for

class PromotionsReply(Reply):
    
    def __init__(self, promotions=None):
        self.promotions = promotions or []

    def to_dict(self):
        return self.promotions

    def to_facebook(self):
        elements = [self._to_facebook_card(promotion) for promotion in self.promotions]
        template = facebook_msg.GenericTemplate(elements)
        attachment = facebook_msg.TemplateAttachment(template)
        message = facebook_msg.Message(attachment=attachment)
        return message

    def _to_facebook_card(self, promotion):
        if promotion['type'] == 'sumo_promotion':
            view_promotion_url = url_for('web.view_promo', promotion_id=promotion['id'])
            claim_promotion_url = url_for('web.claim_promo', promotion_id=promotion['id'])
        elif promotion['type'] == 'internet_deal':
            view_promotion_url = url_for('web.view_deal', promotion_id=promotion['id'])
            claim_promotion_url = url_for('web.claim_deal', promotion_id=promotion['id'])

        default_action = facebook_msg.WebUrlButton('', view_promotion_url)
        view_button = facebook_msg.WebUrlButton('View', view_promotion_url)
        claim_button = facebook_msg.WebUrlButton('Claim', claim_promotion_url)

        element = facebook_msg.Element(title=promotion['name'],
                                       subtitle=promotion['business']['name'][:80],
                                       image_url=promotion['business']['logo'],
                                       default_action=default_action,
                                       buttons=[view_button, claim_button])

        return element

class SearchIntent(Intent):
    
    name = 'search'
    
    def __init__(self, *args, **kwargs):
        super(SearchIntent, self).__init__(*args, **kwargs)
    
    @gen.coroutine
    def process(self, query=''):
        search_url = url_for('api.search', query=query)
        resp = yield self.fetch(search_url)
        data = ujson.loads(resp.body)
        promotions = data['promotions']
        
        if promotions:
            return [PromotionsReply(promotions)]
        else:
            return [TextReply(text="Sorry we can't interpret your message:( Please try again!")]
        
