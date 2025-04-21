import os
import uuid
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class S3ImageUploader:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def download_image(self, url):
        """Download image from URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return ContentFile(response.content)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading image from {url}: {str(e)}")
            raise

    def generate_filename(self, original_url):
        """Generate unique filename for S3"""
        ext = os.path.splitext(urlparse(original_url).path)[1]
        if not ext:
            ext = '.jpg'  # Default extension
        return f"landscapes/{uuid.uuid4()}{ext}"

    def upload_to_s3(self, image_content, filename):
        """Upload image to S3 bucket"""
        try:
            self.s3_client.upload_fileobj(
                image_content,
                self.bucket_name,
                filename,
                ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'}
            )
            return f"https://{self.bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{filename}"
        except ClientError as e:
            logger.error(f"Error uploading to S3: {str(e)}")
            raise

    def process_image_url(self, url):
        """Process image URL and return S3 URL"""
        try:
            image_content = self.download_image(url)
            filename = self.generate_filename(url)
            s3_url = self.upload_to_s3(image_content, filename)
            return s3_url
        except Exception as e:
            logger.error(f"Error processing image {url}: {str(e)}")
            raise