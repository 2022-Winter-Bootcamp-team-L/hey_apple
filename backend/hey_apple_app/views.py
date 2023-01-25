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

from celery.result import AsyncResult


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
    input_image = request.FILES.get('filename')
    task_id = ai_task.delay(input_image)
    return JsonResponse({"task_id": task_id.id})


@api_view(['GET'])
def response_result(request, task_id):
    task = AsyncResult(task_id)
    # print('task : ',task.get('result'))
    if not task.ready():
        return JsonResponse({"ai_resutl" : "notyet"})
    print('result : ', task.get('result'))
    result = task.get('result')
    return JsonResponse({'result' : result})



    # return JsonResponse(data)
# sendEmail API

# exJson = '{"email" : "1106q@naver.com" , "orderbillid" : "2"}'


@api_view(['GET'])
def send_email_api(request):
    result = mail_task(request)

    return result
