import boto3
import botocore
from config.aws import aws_config

class S3Manager(object):
    _url = 'http://{bucket_name}.s3.amazonaws.com/{filename}'

    def __init__(self, aws_secret_access_key=aws_config['secret_access_key'], aws_access_key_id=aws_config['access_key_id'], **kwargs):
        s3_config = kwargs.pop('s3_config', {})

        self.s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, **s3_config)
        self.client = self.s3.meta.client
        self.buckets = {}
     
    def list_buckets(self):
        return self.buckets

    def list_client_buckets(self):
        return self.client.list_buckets()

    def list_bucket_objects(self, bucket_name, **kwargs):
        try:
            bucket = self.buckets[bucket_name]
            resp = self.client.list_objects_v2(Bucket=bucket_name, **kwargs)
            return resp['Contents']
        except:
            raise

    def bucket_exists(self, bucket_name):
        try:
            self.client.head_bucket(Bucket=bucket_name)
            return True
        except botocore.exceptions.ClientError:
            return False

    def get_bucket(bucket_name):
        try:
            return self.buckets[bucket_name]
        except KeyError:
            return self.create_bucket(bucket_name)

    def create_bucket(self, bucket_name):
        if bucket_name in self.buckets:
            return self.buckets[bucket_name]

        if self.bucket_exists(bucket_name):
            self.buckets[bucket_name] = self.s3.Bucket(name=bucket_name)
        else:
            self.buckets[bucket_name] = self.client.create_bucket(Bucket=bucket_name)
        
        return self.buckets[bucket_name]

    def delete_bucket(self, bucket_name):
        try:
            bucket = self.buckets[bucket_name]
            self.client.delete_bucket(Bucket=bucket_name)
            del self.buckets[bucket_name]
        except:
            raise

    def setup_buckets(self, bucket_names):
        for bucket_name in bucket_names:
            self.create_bucket(bucket_name)    

    def get_url(self, bucket_name, filename):
        return self._url.format(bucket_name=bucket_name, filename=filename)    

    def upload_file(self, f, filename, bucket_name, ExtraArgs=None):
        ExtraArgs = ExtraArgs or {
            'ACL': 'public-read'
        }
        try:
            bucket = self.buckets[bucket_name]
            bucket.upload_fileobj(f, filename, ExtraArgs=ExtraArgs)
            return self.get_url(bucket_name, filename)
        except:
            raise
    
    def get_files(self, bucket_name, Prefix=None):
        if not Prefix or not bucket_name:
            return []
        
        try:
            bucket = self.buckets[bucket_name]
            return [obj.key for obj in bucket.objects.filter(Prefix=Prefix)]
        except:
            raise

    def delete_files(self, bucket_name, filenames):
        try:
            delete_objs = []
            for filename in filenames:
                delete_objs.append({
                    'Key': filename
                })
                
            resp = self.buckets[bucket_name].delete_objects(Delete={
                'Objects': delete_objs, 
                'Quiet': True
            })
            return resp
        except:
            raise


