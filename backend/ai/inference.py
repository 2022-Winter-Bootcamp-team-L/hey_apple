import torch
import numpy as np
import cv2
import requests


def ai_inference(url):
    # Model
    model = torch.hub.load('ultralytics/yolov5', 'custom',
                           path="/ai/model_file/best.pt", _verbose=False)

    # Images
    img_name = url.split('/')[-1]
    image_nparray = np.asarray(
        bytearray(requests.get(url).content), dtype=np.uint8)
    img = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)

    h, w, c = img.shape
    new_img = np.zeros((int(h*2.5), int(w*2.5), c), dtype="uint8")

    for i in range(h):
        for j in range(w):
            new_img[i][j] = img[i][j]
    new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
    # Inference
    results = model(new_img)

    # Results
    results.render()  # updates results.ims with boxes and labels
    cv2.imwrite(f"/ai/images/{img_name}",
                results.ims[0][:h+1, :w+1, ::-1])

    return [results.pandas().xyxy[0].values.tolist(), img_name]


if __name__ == "__main__":
    url = 'https://heyapple.s3.ap-northeast-2.amazonaws.com/image/appleorange.jpg'
    # url = 'https://heyapple.s3.ap-northeast-2.amazonaws.com/image/%E1%84%80%E1%85%B2%E1%86%AF.jpeg'
    # url = "https://heyapple.s3.ap-northeast-2.amazonaws.com/image/apples.jpeg"
    # url = "https://heyapple.s3.ap-northeast-2.amazonaws.com/image/%E1%84%89%E1%85%A1%E1%84%80%E1%85%AA.jpeg"
    # url = "https://heyapple.s3.ap-northeast-2.amazonaws.com/image/strawberry.jpeg"
    print(ai_inference(url))
