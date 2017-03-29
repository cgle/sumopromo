from tornado.escape import url_escape

# API
api_search = 'http://localhost:8000/api/v1/search?query={query}'

# WEB
location = lambda x: 'https://8c9a88aa.ngrok.io' + x

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
