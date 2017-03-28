from tornado.escape import url_escape

# API
api_search = 'http://localhost:8000/api/v1/search?query={query}'
api_claim_promo = 'http://localhost:8000/api/v1/claim-promotion?promotion_id={promotion_id}'

# WEB
web_view_promo = 'http://8c9a88aa.ngrok.io/promos/{promotion_id}'

url_maps = {
    'api.search': api_search,
    'api.claim_promo': api_claim_promo,
    'web.view_promo': web_view_promo
}

def url_for(name, **kwargs):
    url = url_maps[name].format(**kwargs).replace(' ', '+')
    return url
