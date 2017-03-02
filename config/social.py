import os, ujson

__all__ = ('social_config',)

config_dir = os.path.dirname(os.path.realpath(__file__))
social_config_path = os.path.join(config_dir, 'social.config')
social_config = ujson.loads(open(social_config_path).read())

