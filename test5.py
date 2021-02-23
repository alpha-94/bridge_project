# 윤곽선 / diff

from skimage import measure, color, filters, metrics
import cv2
import time
import math

cap = cv2.VideoCapture('rtsp://10.0.0.97:554/main&media=video&media=audio')
# cap = cv2.VideoCapture(0)

_, img_base = cap.read()
img_base = cv2.resize(img_base, dsize=(640, 480), interpolation=cv2.INTER_AREA)
img_base = cv2.cvtColor(img_base, cv2.COLOR_BGR2GRAY)
print(img_base.shape)

count = 0
score = 0
custom = 50

while True:
    ret, img_result = cap.read()
    try:
        img_result = cv2.resize(img_result, dsize=(640, 480), interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)

        count += 1
        if count > custom:
            (score, diff_) = metrics.structural_similarity(img_base, img, full=True)
            diff = (diff_ * 255).astype("uint8")
            print("count :: {}  // ssim :: {}".format(count, score))

            count = 0

        cv2.putText(img_result, str(int(score * 100)), (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 1)
        cv2.imshow("rr", img_result)

        if cv2.waitKey(1) & 0xFF == 27:
            break
    except cv2.error as e:
        print(e)
        cap = cv2.VideoCapture('rtsp://10.0.0.97:554/main&media=video&media=audio')
        _, img_base = cap.read()
        img_base = cv2.resize(img_base, dsize=(640, 480), interpolation=cv2.INTER_AREA)
        img_base = cv2.cvtColor(img_base, cv2.COLOR_BGR2GRAY)
        print(img_base.shape)
cv2.destroyAllWindows()
