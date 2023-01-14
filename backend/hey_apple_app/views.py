from rest_framework import viewsets
from rest_framework.decorators import api_view  # @api_view 사용 가능
from rest_framework.response import Response

# from django.core.files.storage import FileSystemStorage #file(image) 관리
from django.core.files.storage import default_storage  # file 저장
from django.http import JsonResponse  # json형으로 반환

from drf_yasg.utils import swagger_auto_schema  # swagger 적용

# from backend.custom_exceptions import * #커스텀 오류 관리용
from rest_framework import exceptions  # 오류 관리용

from .models import image, fruit
from .utils import *
from .serializers import FruitSerializer

from .tasks import ai_task
from PIL import Image
import io


@api_view(['GET'])
def get_fruit(request, id):
    data = fruit.objects.get(id=id)
    serializer = FruitSerializer(data)
    return Response(serializer.data)


@api_view(['POST'])
def get_order_bill(request):
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

    return i_image.s3_image_url
    # return JsonResponse({"s3_image_url": i_image.s3_result_image_url})


@api_view(['POST'])
def get_task_id(request):
    input_image = Image.open(io.BytesIO(request.FILES.get('filename').read()))

    task = ai_task.delay(input_image)
    return JsonResponse({"task_id": task.id})
