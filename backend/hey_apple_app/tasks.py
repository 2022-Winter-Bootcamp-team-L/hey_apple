from __future__ import absolute_import, unicode_literals

from uuid import uuid4

from backend.celery import app
from django.core.files.storage import default_storage
from django.http import JsonResponse

from .models import image, orderpayment, fruitorder,fruit
from .serializers import FruitSerializer
from .utils import s3_connection, s3_put_object, s3_get_image_url
# from .views import get_order_bill
from backend.settings import AWS_STORAGE_BUCKET_NAME
# mail
import logging
import sys
import smtplib
import pymysql
from .error_check import get_secret
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.views import View
from .error_check import error_check_mailAPI_sub
from .inference import ai_inference


@app.task
def ai_task(request, orderpayment_id):
    uuid_key = str(uuid4())  # 고유한 폴더명
    image_uuid = str(uuid4())  # 입력받은 이미지만의 아이디 생성

    file = request
    default_storage.save('ai_image/' + uuid_key + '/' +
    image_uuid + ".jpg", file)  # 입력 받은 이미지 저장

    s3 = s3_connection()  # s3 연결 확인
    s3_upload = s3_put_object(  # s3에 업로드 시도
        s3, AWS_STORAGE_BUCKET_NAME,
        '/backend/ai_image/' + uuid_key + '/' + image_uuid + '.jpg',
        'image/' + image_uuid + '.jpg')
    s3_url = s3_get_image_url(
        s3, 'image/' + str(image_uuid) + '.jpg')  # 업로드 한 이미지 url 가져 오기

    objs, url = ai_inference(s3_url, uuid_key)

    answer = {}
    for obj in objs:
        if obj[6] in answer.keys():
            answer[obj[6]] += 1
        else:
            answer[obj[6]] = 1

    # 하나의 주문에 같이 분석된 이미지들이 공통적으로 가지고 있어야 할 orderpayment가 있는지 확인 후 없다면 생성
    o_orderpayment, is_o_created = orderpayment.objects.get_or_create(id=orderpayment_id)

    # 분석된 이미지 객체 생성
    i_image = image()
    i_image.id = image_uuid
    i_image.orderpayment_id = o_orderpayment
    i_image.s3_image_url = s3_url
    i_image.s3_result_image_url = url
    i_image.save()

    image_price = 0
    result = {}
    fruit_list = []

    
    for key in answer: # 이미지 분석 결과 로직,
        f_fruitorder = fruitorder()
        temp_fruit = fruit.objects.get(name=key)
        f_fruitorder.fruit_id = temp_fruit
        f_fruitorder.image_id = i_image
        f_fruitorder.count = answer[key]
        f_fruitorder.save()

        f_list = {} # 과일 정보
        serializer = FruitSerializer(temp_fruit)
        f_list['fruit_info'] = serializer.data
        f_list['count'] = f_fruitorder.count # 과일 개수
        fruit_list.append(f_list)
        
        image_price += temp_fruit.price * answer[key]
        
    result['fruit_list'] = fruit_list
    i_image.image_price = image_price

    o_orderpayment.save()

    i_image.save() # 이미지 끝

    result['orderpayment_id'] = o_orderpayment.id
    result["image_price"] = image_price
    result["s3_result_image_url"] = url

    return result
    

@app.task
def mail_task(request):

    def mail_check(request):
        global emailcheckFlag
        email = request.GET['email']
        orderpaymentid = request.GET['orderpayment_id']
        if (orderpaymentid is not None) and (email is not None):  # 값이 안들어온 경우 로직 처리 x
            emailcheckFlag = 0  # 초기화
            # 0 : 로직 시작 실패 or 에러 , # 1 : 성공 , # 2 : mail setting #3 dbcon #4 apple_mail
            emailcheckFlag = mail_setting(email, orderpaymentid, emailcheckFlag)
            # print("로직 처리성공 여부 ? : ", emailcheckFlag)
            if emailcheckFlag == 1:  # 내부 함수에서 문제가 생겨 처리가 안된 경우 0으로 반환
                return JsonResponse({"result": "sucess"})
            else:
                error_reason = error_check_mailAPI_sub(emailcheckFlag)
                logging.error(error_reason)
                # 필요하다면 해당 결과 프론트에 줄 수 있긴한데 프론트 만드는 분이랑 팀장님이랑 말해볼것 ..
                return JsonResponse({"result": "false"})
        else:
            return JsonResponse({"result": "false"})

    # mailsetting start
    def mail_setting(email, orderpaymentid, emailcheckFlag):
        if emailcheckFlag == 0:
            # setting start
            global subject
            # parshing start
            try:  # parshing
                subject = email[0:email.index('@')]  # 이메일 아이디 가져오기
            except:
                emailcheckFlag = 2
                return emailcheckFlag
            # parshing end

            emailcheckFlag = 1
            emailcheckFlag = dbcon(email, orderpaymentid, emailcheckFlag)
            return emailcheckFlag

        else:
            emailcheckFlag = 2
            return emailcheckFlag

    # mail setting End

    # dbconnect Start
    def dbcon(email, orderpaymentid, emailcheckFlag):
        if emailcheckFlag == 1:             
            result_total_price = orderpayment.objects.filter(id = orderpaymentid).filter(is_deleted = 0).values('total_price')
            res = result_total_price[0]
            total_price = res['total_price']
            content_img_price = ""
            content_fruit = ""
            result_img = image.objects.filter(orderpayment_id = orderpaymentid).filter(is_deleted = 0).values('id' , "image_price")
            flag =0
            for i in result_img :
                res = result_img[flag]
                img_id = res['id']
                img_price = res['image_price']
                content_img_price += str(img_id) +","+str(img_price)+"\n"

                result_fruitorder = fruitorder.objects.filter(image_id = img_id).filter(is_deleted = 0).values('fruit_id',"count")
                flag2 =0

                for j in result_fruitorder:
                    res= result_fruitorder[flag2]
                    fruit_id = res['fruit_id']
                    result_fruit = fruit.objects.filter(id = fruit_id).filter(is_deleted = 0).values("name" , "price")
                    fruit_info = result_fruit[0]
                    fruit_name =  fruit_info['name']
                    fruit_price = fruit_info['price']
                    fruit_count = res['count']
                    content_fruit += str(fruit_name)+","+str(fruit_price)+","+str(fruit_count)+"\n"  
                    flag2 +=1 
                flag +=1

            emailcheckFlag = 1
            emailcheckFlag = send_mail(
                email, content_img_price, content_fruit,total_price, emailcheckFlag)  # 1
            return emailcheckFlag
        else:
            emailcheckFlag = 3
            return emailcheckFlag

    # dbconnect End

    # mail Send Start
    def send_mail(email, content_img_price, content_fruit,total_price,emailcheckFlag):
        if emailcheckFlag == 1:
            try:  # context 생성 .. 이메일 본문 생성
                print("이미지 : \n" , content_img_price , "과일정보 : \n", content_fruit , "총가격 : ", total_price)
                content = subject+"님 hey, Apple 이용에 감사드립니다."
                content +="이미지별 각 가격입니다. \n"+ content_img_price +"\n"+"과일정보 입니다. \n"+content_fruit+"\n\n"+"총가격입니다.\n"
                content +="URL"
            except:
                emailcheckFlag = 4
                return emailcheckFlag
            try:  # mail Sent
                smtp = smtplib.SMTP('smtp.gmail.com', 587)
                smtp.starttls()
                GOGLE_MAIL_KEY = get_secret("GOGLE_MAIL_KEY")
                GOGLE_EMAIL = get_secret("GOGLE_EMAIL")
                smtp.login(GOGLE_EMAIL, GOGLE_MAIL_KEY)

                msg = MIMEText(content)
                msg['Subject'] = subject + "님 감사드립니다."
                msg['From'] = "hey,Apple"
                msg['To'] = email
                smtp.sendmail(GOGLE_EMAIL, email, msg.as_string())
                smtp.quit()
            except:
                emailcheckFlag = 4
                return emailcheckFlag

            emailcheckFlag = 1
            return emailcheckFlag
        else:
            emailcheckFlag = 4
            return emailcheckFlag
    # mail Send End
    result = mail_check(request)
    return result  # 결과값 전송 : {"result" : "sucess or false"}
