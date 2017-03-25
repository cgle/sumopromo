from config.social import social_config

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'dev_sumopromo_cookie'

    WTF_CSRF_SECRET_KEY = 'dev_sumopromo_csrf'

    OAUTH_CREDENTIALS = {
        'google': {
            'id': social_config['google']['client_id'],
            'secret': social_config['google']['client_secret']
        },
        'facebook': {
            'id': social_config['facebook']['consumer_key'],
            'secret': social_config['facebook']['consumer_secret']
        }
    }
    
    GOOGLE_MAP_API_KEY = social_config['google']['map_api_key']

    S3_BUCKETS = {
        'user': 'sumopromo.user', 
        'business': 'sumopromo.business', 
        'promotion': 'sumopromo.promotion',
    }
    
    DEMO = True

class DevConfig(Config):
    DEBUG = True
    TESTING = True

class ProdConfig(Config):
    DEBUG = False
    TESTING = False
