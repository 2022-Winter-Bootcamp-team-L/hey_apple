from rest_framework import viewsets
from rest_framework.decorators import api_view # @api_view 사용 가능


from django.core.files.storage import FileSystemStorage #file(image) 관리
from django.http import JsonResponse # json형으로 반환

from drf_yasg.utils import swagger_auto_schema # swagger 적용

# from backend.custom_exceptions import * #커스텀 오류 관리용
from rest_framework import exceptions # 오류 관리용

from hey_apple_app.models import Fruit
# from hey_apple_app.serializers import FruitSerializer


# Create your views here.

# api 예제
@api_view(['GET'])
def get_fruit(request):
    
    #Fruit를 볼 수 있는 view
    queryset = Fruit.objects.all() # 형변환 필요, 그대로 사용하면 오류남
    return JsonResponse({"result": "queryset"})