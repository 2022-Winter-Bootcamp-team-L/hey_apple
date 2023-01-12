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

# mail API
import logging
import sys
import smtplib
import pymysql
from .error_check import error_check_mailAPI_sub , get_secret
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.views import View

# Create your views here.

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
        data = cache.get_or_set(id, fruit.objects.get(id=id))  # timeout 설정 고민
        serializer = FruitSerializer(data)
        return Response(serializer.data)
    except fruit.DoesNotExist as e:
        logging.error(f"fruit_id: {id} does not exist")
        return JsonResponse({"error": "error_page"})


@api_view(['POST'])
def get_order_bill(request):
    uuidKey = str(uuid4())  # 고유한 폴더명
    imageName = str(uuid4())  # 입력받은 이미지만의 아이디 생성

    file = request.FILES['filename']  # 입력받은 이미지
    default_storage.save('ai_image/'+uuidKey+'/' +
                         imageName+".jpg", file)  # 입력받은 이미지 저장

    s3 = s3_connection()  # s3 연결 확인
    s3_upload = s3_put_object(  # s3에 업로드 시도
        s3, AWS_STORAGE_BUCKET_NAME,
        '/backend/ai_image/' + uuidKey + '/' + imageName + '.jpg',
        'image/' + imageName + '.jpg')
    s3_url = s3_get_image_url(
        s3, 'image/' + str(imageName) + '.jpg')  # 업로드한 이미지 url 가져오기

    iImage = image()
    iImage.id = imageName
    iImage.s3_image_url = s3_url
    iImage.s3_result_image_url = s3_url
    iImage.save()
    
# sendEmail API 
             
#exJson = '{"email" : "1106q@naver.com" , "orderbillid" : "2"}'
def send_email_api(request):
    global emailcheckFlag
    email = request.GET['email']
    orderbillid = request.GET['orderbillid']
    if (orderbillid is not None) or (email is not None): #값이 안들어온 경우 로직 처리 x
        emailcheckFlag = 0 # 초기화
        # 0 : 로직 시작 실패 or 에러 , # 1 : 성공 , # 2 : mail setting #3 dbcon #4 apple_mail
        emailcheckFlag = mail_setting(email,orderbillid,emailcheckFlag)
        #print("로직 처리성공 여부 ? : ", emailcheckFlag)
        if emailcheckFlag == 1: # 내부 함수에서 문제가 생겨 처리가 안된 경우 0으로 반환 
            return JsonResponse({"result": "sucess"})
        else :
            error_reason = error_check_mailAPI_sub(emailcheckFlag)
            logging.error(error_reason)
            #필요하다면 해당 결과 프론트에 줄 수 있긴한데 프론트 만드는 분이랑 팀장님이랑 말해볼것 .. 
            return JsonResponse({"result": "false"})
    else:
        return JsonResponse({"result": "false"})

def mail_setting(email,orderbillid,emailcheckFlag):
    if emailcheckFlag == 0 :
        #setting start
        global subject
        # parshing start
        try: #parshing
            subject = email[0:email.index('@')] #이메일 아이디 가져오기
        except :
            emailcheckFlag=2
            return emailcheckFlag
        # parshing end
        
        emailcheckFlag=1 
        emailcheckFlag = dbcon(email,orderbillid,emailcheckFlag)
        return emailcheckFlag
    
    else :
        emailcheckFlag=2
        return emailcheckFlag
    
#mail setting End

#dbconnect Start
def dbcon(email,orderbillid,emailcheckFlag):
    if emailcheckFlag == 1 :
        email = email
        global saveInfo
        try: #connect 
            db = pymysql.Connect(host='db' ,user="root" , password="1234", database="mysql-db")
            cursor = db.cursor()
        except :
            emailcheckFlag = 3
            return emailcheckFlag
        try: # query serch
            query="select total_price from orderbill where id ="+orderbillid 
            cursor.execute(query)
            result = cursor.fetchone()
            totalPrice = result[0]

            
            query2="select Distinct fruit_id , count from fruitorderbill where orderbill_id ="+orderbillid
            cursor.execute(query2)
            result = cursor.fetchall()
            saveInfo= [[0 for col in range(3)] for row in range(len(result))] #col 열 row 행
            
            flag = 0
            
            for i ,k in result:
                count = k
                #Fruit name , price 조회 start
                query3 = "select name , price from fruit where id ="+str(i)
                cursor.execute(query3)
                results= cursor.fetchall()
                saveInfo[flag][2] =  count
                
                for i , j in results:
                    name =i
                    price = j
                    saveInfo[flag][0] = name
                    saveInfo[flag][1] = price
                    flag +=1
                #Fruit name , price 조회 end
        except:
            emailcheckFlag = 3
            return emailcheckFlag 
          
        emailcheckFlag =1
        emailcheckFlag = send_mail(email ,saveInfo, totalPrice, emailcheckFlag) #1 
        return emailcheckFlag
    else :
        emailcheckFlag = 3
        return emailcheckFlag
            
#dbconnect End

#mail Send Start
def send_mail(email , saveInfo, totalPrice, emailcheckFlag):
    if emailcheckFlag == 1:
        try: # context 생성 .. 이메일 본문 생성
            context = "   Hey Apple 사용에 감사드립니다. " + subject +"님"+ "\n\n\n"
            for i in range(len(saveInfo)):
                for j in range(len(saveInfo[i])): # name , price , count
                    contea = saveInfo[i][j]
                    context = context +" "+str(contea)
                context +="\n"
            context = context + "\n 총가격 : " + str(totalPrice) +"\n url 넣을 공간"
        except:
            emailcheckFlag = 4
            return emailcheckFlag
        try: #mail Sent
            smtp = smtplib.SMTP('smtp.gmail.com',587)
            smtp.starttls()
            GOGLE_MAIL_KEY= get_secret("GOGLE_MAIL_KEY")
            smtp.login('testproject9197@gmail.com',GOGLE_MAIL_KEY)


            msg = MIMEText(context)
            msg['Subject'] = subject +"님 감사드립니다."
            msg['From']= "hey,Apple"
            msg['To']= email
            smtp.sendmail('testproject9197@gmail.com',email,msg.as_string())
            smtp.quit()  
        except:
            emailcheckFlag = 4
            return emailcheckFlag
        
        emailcheckFlag = 1
        return emailcheckFlag
    else:
        emailcheckFlag = 4
        return emailcheckFlag
#mail Send End