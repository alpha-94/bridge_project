# RGB 찾기 + ROI

import cv2
import numpy as np
import pytesseract

capture = cv2.VideoCapture('rtsp://10.0.0.97:554/main&media=video&media=audio')
print('image width %d' % capture.get(3))
print('image height %d' % capture.get(4))


# capture.set(3, 480)
# capture.set(4, 640)

def mouse_callback(event, x, y, flags, param):
    global hsv

    # 마우스 왼쪽 버튼 누를시 위치에 있는 픽셀값을 읽어와서 HSV로 변환합니다.
    if event == cv2.EVENT_LBUTTONDOWN:
        print('x : {}, y : {}'.format(x, y))
        color = frame[y, x]

        one_pixel = np.uint8([[color]])
        hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
        print('hsv1 : ', hsv)
        hsv = hsv[0][0]
        print('hsv2 : ', hsv)


def custom_hsv(x, y):
    color = frame[x, y]
    one_pixel = np.uint8([[color]])
    hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
    hsv = hsv[0][0]
    h, s, v = hsv
    return h, s, v


def mopology(result, clr, div_value):
    # mopology
    kernelOpen = np.ones((5, 5))
    kernelClose = np.ones((20, 20))

    maskOpen = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose
    conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(img, conts, -1, (255, 0, 0), 3)

    if conts:
        if clr == (255, 0, 0):
            # print('blue')
            pass
        elif clr == (0, 255, 0):
            # print('green')
            pass
        else:
            # print('red')
            pass

    for i in range(len(conts)):
        x, y, w, h = cv2.boundingRect(conts[i])

        x += div_value
        cv2.rectangle(frame, (x, y), (x + w, y + h), clr, 2)


cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouse_callback)

while 1:
    ret, frame = capture.read()
    frame = cv2.resize(frame, dsize=(640, 480), interpolation=cv2.INTER_AREA)

    h, w, _ = frame.shape

    div1_value = int(w / 3)
    div2_value = int(2 * w / 3)

    div1 = frame[0:h, 0:div1_value]
    div2 = frame[0:h, div1_value + 1:div2_value]
    div3 = frame[0:h, div2_value + 1:w]

    # print('div1 : {0} div2 : {1} div3 : {2}'.format(0, int(w / 3) + 1, int(2 * w / 3)))

    if ret:
        # 중앙 좌표점
        cv2.circle(frame, (int(w / 2), int(h / 2)), 3, (0, 255, 255), -1)

        # 구분선
        cv2.line(frame, (int(w / 3), 0), (int(w / 3), h), (0, 255, 255), 1)
        cv2.line(frame, (int(2 * w / 3), 0), (int(2 * w / 3), h), (0, 255, 255), 1)

        # 구분
        cv2.putText(div1, '1', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.putText(div2, '2', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.putText(div3, '3', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)

        img = cv2.cvtColor(div1, cv2.COLOR_BGR2HSV)

        # text area

        # text = cv2.cvtColor(div1, cv2.COLOR_BGR2GRAY)
        # text = cv2.threshold(text, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # text = cv2.medianBlur(text, 10)
        # cv2.imshow("text", text)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        # text = pytesseract.image_to_string(text)
        # print(text)

        # Blue section in image
        hsv_B = custom_hsv(110, 360)
        h, s, v = hsv_B

        lowerBound_B = np.array([h-10, s-10, v-10])
        upperBound_B = np.array([h+30, s+30, v+30])

        blue = (255, 0, 0)
        cv2.circle(frame, (110, 360), 3, blue, -1)

        mask_b = cv2.inRange(img, lowerBound_B, upperBound_B)

        # Green section in image
        hsv_G = custom_hsv(120, 221)
        h, s, v = hsv_G

        lowerBound_G = np.array([h-10, s-10, v-10])
        upperBound_G = np.array([h+10, s+10, v+10])

        green = (0, 255, 0)
        cv2.circle(frame, (120, 221), 3, green, -1)

        mask_g = cv2.inRange(img, lowerBound_G, upperBound_G)

        # Red section in image
        hsv_R = custom_hsv(93, 90)
        h, s, v = hsv_R

        lowerBound_R = np.array([h-10, s-10, v-10])
        upperBound_R =np.array([h+10, s+10, v+10])

        red = (0, 0, 255)
        cv2.circle(frame, (93, 90), 3, red, -1)

        mask_r = cv2.inRange(img, lowerBound_R, upperBound_R)

        mopology(mask_b, blue, 0)

        mopology(mask_g, green, 0)

        mopology(mask_r, red, 0)

        cv2.imshow("mask_b", mask_b)
        cv2.imshow("mask_g", mask_g)
        cv2.imshow("mask_r", mask_r)

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
