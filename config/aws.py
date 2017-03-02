import os, ujson

__all__ = ('aws_config',)

config_dir = os.path.dirname(os.path.realpath(__file__))
aws_config_path = os.path.join(config_dir, 'aws.config')
aws_config = ujson.loads(open(aws_config_path).read())

