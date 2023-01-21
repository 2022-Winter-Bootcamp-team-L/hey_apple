import logging
from rest_framework.views import APIView, exceptions
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view  # @api_view 사용 가능
from rest_framework.response import Response

from django.http import JsonResponse  # json형으로 반환
from django.core.cache import cache

from drf_yasg.utils import swagger_auto_schema  # swagger 적용
from drf_yasg import openapi

from .models import fruit
from .utils import *
from .serializers import FruitSerializer

from .tasks import ai_task

# mail API
from .tasks import mail_task
import logging

from celery.result import AsyncResult
from uuid import uuid4


class FruitsInfo(APIView):
    id = openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='원하는 과일 id를 입력하세요.')
    @swagger_auto_schema(manual_parameters=[id])
    def get(self, request, id):
        try:
            obj = fruit.objects.get(id=id)
            serializer = FruitSerializer(obj)
            data = cache.get_or_set(id, serializer.data)  # timeout 설정 고민
            return Response(data)
        except fruit.DoesNotExist as e:
            logging.error(f"fruit_id: {id} does not exist")
        return JsonResponse({"error": "error_page"})

class FruitsImage(APIView):
    parser_classes = [MultiPartParser]
    
    type = openapi.Parameter('filename',openapi.IN_FORM, type=openapi.TYPE_FILE, description='주문할 과일이 찍힌 사진을 선택해주세요.')
    @swagger_auto_schema(manual_parameters=[type])
    
    def post(self, request):
        image_list = request.FILES.getlist('filename')
        task_id_list = {}
        num = 1
        orderpayment_id = uuid4()

        for image in image_list:
            task_id = ai_task.delay(image, orderpayment_id)
            task_id_list['task_id'+str(num)] = task_id.id
            num = num+1
        return JsonResponse({"result": task_id_list}) 

class FruitsPayment(APIView):
    task_id = openapi.Parameter('task_id', openapi.IN_PATH, type=openapi.TYPE_STRING, description='task_id를 입력하세요.')
    @swagger_auto_schema(manual_parameters=[task_id])
    def get(self, request, task_id):
        task = AsyncResult(task_id)
        if not task.ready():
            return JsonResponse({"ai_resutl" : "notyet"})
        print('result : ', task.get('result'))
        result = task.get('result')
        return JsonResponse({'result' : result})

# sendEmail API
# exJson = '{"email" : "1106q@naver.com" , "orderbillid" : "2"}'

class EmailPost(APIView):
    email = openapi.Parameter('email', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='email를 입력하세요.')
    orderpayment_id = openapi.Parameter('orderpayment_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='orderpayment_id를 입력하세요.')
    @swagger_auto_schema(manual_parameters=[email,orderpayment_id])
    def get(self, request):
        result = mail_task(request)
        return result

# @ api_view(['GET'])
# def send_email_api(request):
#     result = mail_task(request)

#     return result
