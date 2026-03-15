import os
import json
import datetime as dt
import boto3

from dotenv import load_dotenv
from botocore.config import Config

class MinioClient():

    def __init__(self):
        load_dotenv()

        self.endpoint = os.getenv("MINIO_ENDPOINT")
        self.access_key = os.getenv("MINIO_ROOT_USER")
        self.secret_key = os.getenv("MINIO_ROOT_PASSWORD")
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME")

        self.client = boto3.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(
                signature_version='s3v4'
            )
        )

        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except:
            self.client.create_bucket(Bucket=self.bucket_name)

    def _create_path(self, source, entity):
        date = dt.datetime.now()
        path = f"{source}/{entity}/{date.year}/{date.month:02d}/{date.day:02d}/{entity}_{date.strftime('%d%m%Y_%H%M%S')}.json"
        return path

    def save_data(self, data, source="opendota", entity=None):
        data = json.dumps(data, indent=2, ensure_ascii=False)

        self.client.put_object(
            Bucket=self.bucket_name,
            Key=self._create_path(source, entity),
            Body=data.encode('utf-8'),
            ContentType='application/json'
        )
