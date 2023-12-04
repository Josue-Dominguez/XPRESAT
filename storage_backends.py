from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_ac1 = 'private'


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_ac1 = 'private'
    file_overwrite = False