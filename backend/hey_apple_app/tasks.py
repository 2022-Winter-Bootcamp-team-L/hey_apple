from __future__ import absolute_import, unicode_literals

from uuid import uuid4

from backend.celery import app
from django.core.files.storage import default_storage
from django.http import JsonResponse

from .models import image
from .utils import s3_connection, s3_put_object, s3_get_image_url
# from .views import get_order_bill
from backend.settings import AWS_STORAGE_BUCKET_NAME


@app.task
def ai_task(request):
    # url = get_order_bill(request)
    uuid_key = str(uuid4())  # 고유한 폴더명
    image_name = str(uuid4())  # 입력받은 이미지만의 아이디 생성

    file = request.FILES['filename']  # 입력받은 이미지
    default_storage.save('ai_image/' + uuid_key + '/' + image_name + ".jpg", file)  # 입력 받은 이미지 저장

    s3 = s3_connection()  # s3 연결 확인
    s3_upload = s3_put_object(  # s3에 업로드 시도
        s3, AWS_STORAGE_BUCKET_NAME,
        '/backend/ai_image/' + uuid_key + '/' + image_name + '.jpg',
        'image/' + image_name + '.jpg')
    s3_url = s3_get_image_url(s3, 'image/' + str(image_name) + '.jpg')  # 업로드 한 이미지 url 가져 오기

    i_image = image()
    i_image.id = image_name
    i_image.s3_image_url = s3_url
    i_image.s3_result_image_url = s3_url
    i_image.save()

    url = i_image.s3_image_url
# ai task

    return JsonResponse({"image_url": url})
