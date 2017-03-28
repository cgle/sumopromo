import logging
from database import metadata
from database.sumodb import SumoDB
from config.db import database_uri, engine_options, session_options

from drivers.s3 import S3Manager
from config.aws import aws_config

def setup_db():
    print('drop and init sumodb')
    sumo_db = SumoDB(database_uri, metadata=metadata, engine_options=engine_options, session_options=session_options)
    sumo_db.drop_all()
    sumo_db.create_all()

    sumo_db.category.create_from_list(['food drink','restaurant','groceries','bakery','beauty spas','health fitness','salon','gym','travel','pets','retail'])
    
    demo_user = sumo_db.user.add(email='demo@sumo.promo', password='demo', first_name='DEMO', last_name='DEMO')

def cleanup_aws():
    s3 = S3Manager(aws_secret_access_key=aws_config['secret_access_key'],
                   aws_access_key_id=aws_config['access_key_id'])

    buckets = ['sumopromo.business', 'sumopromo.user', 'sumopromo.promotion']
    s3.setup_buckets(buckets)

    
    for bucket in buckets:
        try:
            print('Deleting objects from {} bucket'.format(bucket))
            s3.delete_all_bucket_objects(bucket)
            print('Done deleting from {} bucket'.format(bucket))
        except Exception as e:
            print('Error {}'.format(e))


def generate_fake_data():
    pass

if __name__ == '__main__':
    setup_db()
    cleanup_aws()
