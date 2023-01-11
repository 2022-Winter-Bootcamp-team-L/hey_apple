from rest_framework import viewsets
from rest_framework.decorators import api_view # @api_view 사용 가능


# from django.core.files.storage import FileSystemStorage #file(image) 관리
from django.core.files.storage import default_storage #file 저장
from django.http import JsonResponse # json형으로 반환

from drf_yasg.utils import swagger_auto_schema # swagger 적용

# from backend.custom_exceptions import * #커스텀 오류 관리용
from rest_framework import exceptions # 오류 관리용


from .models import images
from .utils import *
# from hey_apple_app.serializers import FruitSerializer


# Create your views here.

# api 예제
@api_view(['GET'])
def get_fruit(request):
    #Fruit를 볼 수 있는 view
    queryset = Fruit.objects.all() # 형변환 필요, 그대로 사용하면 오류남
    return JsonResponse({"result": "queryset"})


@api_view(['POST'])
def get_order_bill(request):
    uuidKey = str(uuid4()) #고유한 폴더명
    imageName = str(uuid4()) # 입력받은 이미지만의 아이디 생성

    file = request.FILES['filename'] #입력받은 이미지
    default_storage.save('ai_image/'+uuidKey+'/'+imageName+".png", file) #입력받은 이미지 저장 

    s3 = s3_connection() # s3 연결 확인
    s3_upload = s3_put_object( # s3에 업로드 시도
            s3, AWS_STORAGE_BUCKET_NAME,
            '/app/media/' + str(imageName) + '.png',
            'image/' + str(imageName) + '.png')
    s3_url = s3_get_image_url(s3, 'image/' + str(imageName) + '.png') #업로드한 이미지 url 가져오기

    image = Image()
    image.s3_image_url = s3_url
    image.s3_result_image_url = s3_url
    image.save()
    

