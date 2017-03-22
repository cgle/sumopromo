class Config(object):
    
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

    MAX_THREADS = 16
    MAX_WORKERS = 8
