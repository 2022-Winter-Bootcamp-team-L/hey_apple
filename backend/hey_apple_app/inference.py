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
                           path="/backend/hey_apple_app/model_file/best_eng.pt", _verbose=False)

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

    colors = {
        0: (255, 56, 56),
        1: (255, 157, 151),
        2: (255, 178, 29),
        3: (207, 210, 49),
        4: (72, 249, 10),
        5: (146, 204, 23),
        6: (61, 219, 134),
        7: (26, 147, 52),
        8: (0, 212, 187),
        9: (44, 153, 168),
        10: (0, 194, 255),
        11: (132, 56, 255),
    }
    lw = max(round((h + w) / 2 * 0.003), 2)
    font_color = (255, 255, 255)
    # Results
    fruits = results.pandas().xyxy[0].values.tolist()
    for fruit in fruits:
        p1 = (int(fruit[0]), int(fruit[1]))
        p2 = (int(fruit[2]), int(fruit[3]))
        cv2.rectangle(img, p1, p2, colors[fruit[5]], lw, lineType=cv2.LINE_AA)

        # label
        tf = max(lw-1, 1)
        w, h = cv2.getTextSize(fruit[6], 0, fontScale=lw / 3, thickness=tf)[0]
        p2 = (p1[0] + w, p1[1] - h - 3)
        cv2.rectangle(img, p1, p2, colors[fruit[5]], -1, cv2.LINE_AA)
        cv2.putText(img, fruit[6], (p1[0], p1[1] - 2), 0,
                    lw/3, font_color, thickness=tf, lineType=cv2.LINE_AA)
    cv2.imwrite('/backend/ai_image/' + folder_name + '/' + "detected_" + image_name + '.jpg',
                img)

    s3 = s3_connection()  # s3 연결 확인

    s3_upload = s3_put_object(  # s3에 업로드 시도
        s3, AWS_STORAGE_BUCKET_NAME,
        '/backend/ai_image/' + folder_name + '/' + "detected_" + image_name + '.jpg',
        'image/detected_' + image_name + '.jpg')

    s3_url = s3_get_image_url(
        s3, 'image/detected_' + image_name + '.jpg')

    return [results.pandas().xyxy[0].values.tolist(), s3_url]
