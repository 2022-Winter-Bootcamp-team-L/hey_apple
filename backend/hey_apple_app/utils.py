from fileinput import filename
from unicodedata import name
from PIL import Image, ImageOps  # pillow 사용
from uuid import uuid4  # uuid 생성
import boto3, os
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from backend.settings import AWS_REGION, AWS_STORAGE_BUCKET_NAME


def s3_connection():
    """
    s3 bucket에 연결하는 함수
    """
    s3 = boto3.client('s3', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return s3


def s3_put_object(s3, bucket, filepath, filename):
    """
    s3 bucket에 파일 업로드
    """
    try:
        s3.upload_file(filepath, bucket, filename)
    except Exception as e:
        print(e)
        return False
    return True


def s3_get_image_url(s3, filename: str):
    """
    image url을 불러오는 함수
    """
    return f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}'


def get_img_url(img):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    image = img
    image_type = "jpg"
    image_uuid = str(uuid4())
    s3_client.put_object(Body=image, Bucket=AWS_STORAGE_BUCKET_NAME, Key=image_uuid + "." + image_type)
    image_url = f"http://{AWS_STORAGE_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/" + \
                image_uuid + "." + image_type
    image_url = image_url.replace(" ", "/")
    return image_url