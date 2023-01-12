from rest_framework import viewsets
from rest_framework.decorators import api_view  # @api_view 사용 가능
from rest_framework.response import Response


# from django.core.files.storage import FileSystemStorage #file(image) 관리
from django.core.files.storage import default_storage #file 저장
from django.http import JsonResponse # json형으로 반환




from drf_yasg.utils import swagger_auto_schema  # swagger 적용

# from backend.custom_exceptions import * #커스텀 오류 관리용
from rest_framework import exceptions  # 오류 관리용


from .models import image, fruit
from .utils import *
from .serializers import FruitSerializer



# Create your views here.

@api_view(['GET'])
def get_fruit(request, id):
    data = fruit.objects.get(id=id)
    serializer = FruitSerializer(data)
    return Response(serializer.data)

@api_view(['POST'])
def get_order_bill(request):
    uuidKey = str(uuid4()) #고유한 폴더명
    imageName = str(uuid4()) # 입력받은 이미지만의 아이디 생성

    file = request.FILES['filename'] #입력받은 이미지
    default_storage.save('ai_image/'+uuidKey+'/'+imageName+".jpg", file) #입력받은 이미지 저장 

    s3 = s3_connection() # s3 연결 확인
    s3_upload = s3_put_object( # s3에 업로드 시도
            s3, AWS_STORAGE_BUCKET_NAME,
            '/backend/ai_image/' + uuidKey + '/' + imageName + '.jpg',
            'image/' + imageName + '.jpg')
    s3_url = s3_get_image_url(s3, 'image/' + str(imageName) + '.jpg') #업로드한 이미지 url 가져오기

    iImage = image()
    iImage.id = imageName
    iImage.s3_image_url = s3_url
    iImage.s3_result_image_url = s3_url
    iImage.save()
    
