from tornado.escape import url_escape

from chatbot.config import config

location = lambda x: config.web_location_base + x

# API
api_search = location('/api/v1/search?query={query}')

# WEB

web_view_promo = location('/promos/{promotion_id}')
web_claim_promo = location('/promos/{promotion_id}/claim')

#ACCOUNT
account_login = location('/login')
account_logout = location('/logout')
account_fb_auth = location('/auth/facebook')

url_maps = {
    'api.search': api_search,

    'account.login': account_login,
    'account.logout': account_logout,
    'account.facebook_auth': account_fb_auth,

    'web.view_promo': web_view_promo,
    'web.claim_promo': web_claim_promo
}

def url_for(name, **kwargs):
    url = url_maps[name].format(**kwargs).replace(' ', '+')
    return url
