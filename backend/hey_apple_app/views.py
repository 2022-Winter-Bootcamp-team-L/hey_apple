import logging
from rest_framework import viewsets
from rest_framework.decorators import api_view  # @api_view 사용 가능
from rest_framework.response import Response

# from django.core.files.storage import FileSystemStorage #file(image) 관리
from django.core.files.storage import default_storage  # file 저장
from django.http import JsonResponse  # json형으로 반환
from django.core.cache import cache

from drf_yasg.utils import swagger_auto_schema  # swagger 적용

# from backend.custom_exceptions import * #커스텀 오류 관리용
from rest_framework import exceptions  # 오류 관리용

from .models import image, fruit
from .utils import *
from .serializers import FruitSerializer

from .tasks import ai_task
from PIL import Image
import io

# mail API
from .tasks import mail_task
import logging



@api_view(['GET'])
def get_fruit(request, id):
    # data = cache.get(id)
    # if data is None:
    #     data = fruit.objects.get(id=id)
    #     serializer = FruitSerializer(data)
    #     cache.set(id, serializer.data)
    #     print("get mysql")
    #     return Response(serializer.data)
    # print("get redis")
    try:
        obj = fruit.objects.get(id=id)
        serializer = FruitSerializer(obj)
        data = cache.get_or_set(id, serializer.data)  # timeout 설정 고민
        return Response(data)
    except fruit.DoesNotExist as e:
        logging.error(f"fruit_id: {id} does not exist")
        return JsonResponse({"error": "error_page"})


@api_view(['POST'])
def get_task_id(request):
    input_image = Image.open(io.BytesIO(request.FILES.get('filename').read()))

    task = ai_task.delay(input_image)
    return JsonResponse({"task_id": task.id})
    '''
        '/backend/ai_image/' + uuidKey + '/' + imageName + '.jpg',
        'image/' + imageName + '.jpg')
    s3_url = s3_get_image_url(
        s3, 'image/' + str(imageName) + '.jpg')  # 업로드한 이미지 url 가져오기

    iImage = image()
    iImage.id = imageName
    iImage.s3_image_url = s3_url
    iImage.s3_result_image_url = s3_url
    iImage.save()
    '''
# sendEmail API 
             
#exJson = '{"email" : "1106q@naver.com" , "orderbillid" : "2"}'
def send_email_api(request):
    result = mail_task(request)

    return result