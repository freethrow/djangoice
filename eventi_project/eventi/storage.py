# eventi/storage.py
from storages.backends.s3boto3 import S3Boto3Storage


class BackblazeB2Storage(S3Boto3Storage):
    """
    Custom storage for Backblaze B2
    """

    location = "event_files"  # Optional subfolder in your bucket
