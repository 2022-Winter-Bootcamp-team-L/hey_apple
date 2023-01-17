from backend.settings import AWS_STORAGE_BUCKET_NAME
from .utils import s3_connection, s3_get_image_url, s3_put_object
import torch
import numpy as np
import cv2
import requests
from uuid import uuid4


def ai_inference(url, folder_name):
    # Model
    model = torch.hub.load('ultralytics/yolov5', 'custom',
    path="/backend/hey_apple_app/model_file/best.pt", _verbose=False)

    # Images
    image_nparray = np.asarray(
        bytearray(requests.get(url).content), dtype=np.uint8)
    img = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)

    # 2.5배 된 이미지에 원본 이미지 덮어쓰기
    h, w, c = img.shape
    new_img = np.zeros((int(h*2.5), int(w*2.5), c), dtype="uint8")

    for i in range(h):
        for j in range(w):
            new_img[i][j] = img[i][j]

    # BGR to RGB
    new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)

    # Inference
    results = model(new_img)

    # Results
    image_name = str(uuid4())  # 입력받은 이미지만의 아이디 생성

    results.render()  # updates results.ims with boxes and labels
    cv2.imwrite('/backend/ai_image/' + folder_name + '/' + "detected_" + image_name + '.jpg',
                results.ims[0][:h+1, :w+1, ::-1])

    s3 = s3_connection()  # s3 연결 확인

    s3_upload = s3_put_object(  # s3에 업로드 시도
        s3, AWS_STORAGE_BUCKET_NAME,
        '/backend/ai_image/' + folder_name + '/' + "detected_" + image_name + '.jpg',
        'image/detected_' + image_name + '.jpg')

    s3_url = s3_get_image_url(
        s3, 'image/detected_' + image_name + '.jpg')

    return [results.pandas().xyxy[0].values.tolist(), s3_url]


if __name__ == "__main__":
    url = 'https://heyapple.s3.ap-northeast-2.amazonaws.com/image/appleorange.jpg'
    # url = 'https://heyapple.s3.ap-northeast-2.amazonaws.com/image/%E1%84%80%E1%85%B2%E1%86%AF.jpeg'
    # url = "https://heyapple.s3.ap-northeast-2.amazonaws.com/image/apples.jpeg"
    # url = "https://heyapple.s3.ap-northeast-2.amazonaws.com/image/%E1%84%89%E1%85%A1%E1%84%80%E1%85%AA.jpeg"
    # url = "https://heyapple.s3.ap-northeast-2.amazonaws.com/image/strawberry.jpeg"
    print(ai_inference(url))
