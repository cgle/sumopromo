from config.social import social_config

class Config(object):
    
    MAX_THREADS = 16
    MAX_WORKERS = 8    
    
    web_location_base = 'http://demo.sumopromo.com'
    #web_location_base = 'https://8c9a88aa.ngrok.io'

    app = {
        'compress_response': True,
        'debug': True,
        'cookie_secret': 'sumo_promo_chatbot',
        'cookie_expires': 31
    }

    server = {
        'port': 9000,
        'host': '0.0.0.0',
        'num_workers': 1
    }

    social = social_config
