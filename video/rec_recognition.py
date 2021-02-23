from skimage import measure, color, filters, metrics
import cv2
from imutils.video import VideoStream
import time
import math
import numpy as np


class Rectangle_Recognition:
    def __init__(self):
        self.cap = VideoStream('rtsp://10.0.0.97:554/main&media=video&media=audio').start()
        self.none_array = []
        self.else_array = []
        self.test = []

    def setLabel(self, img, pts, label, move_point=None):
        if move_point is None:
            (x, y, w, h) = cv2.boundingRect(pts)
            pt1 = (x, y)
            pt2 = (x + w, y + h)
            if 70 > h > 60 and 70 > w > 50:
                # print("x :: {}, y :: {}, w :: {}, h :: {}".format(x, y, w, h))
                cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
                cv2.putText(img, 'w :: {}, h :: {}'.format(w, h), (pt1[0], pt1[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 255))
                self.none_array.append(1)

            else:
                self.none_array.append(0)

            if len(self.none_array) == 1000:
                a = np.array(self.none_array).sum()
                # print('a :: {}, len(array) :: {}'.format(a, len(array)))
                if a > 10:
                    print('score(%) :: ', round(a / len(self.none_array) * 100, 2), '%')
                    if a / len(self.none_array) * 100 > 2.5:
                        self.test.append(1)
                    else:
                        self.test.append(0)

                print('test score :: {} %'.format(round(np.count_nonzero(self.test) / len(self.test) * 100)))
                print('test 1_count :: {} / len :: {}'.format(np.count_nonzero(self.test), len(self.test)))
                self.none_array.clear()

        else:
            (x, y, w, h) = cv2.boundingRect(pts)
            pt1 = (x + move_point, y)
            pt2 = (x + w + move_point, y + h)
            if h > 22 and w > 80:
                # print("x :: {}, y :: {}, w :: {}, h :: {}".format(x, y, w, h))
                cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
                cv2.putText(img, 'w :: {}, h :: {}'.format(w, h), (pt1[0], pt1[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 255))

    def stream(self):
        img = self.cap.read()
        img = cv2.resize(img, dsize=(640, 480), interpolation=cv2.INTER_AREA)
        h, w, _ = img.shape

        div1_value = int(w / 3)
        div2_value = int(2 * w / 3)

        div1 = img[0:h, 0:div1_value]
        div2 = img[0:h, div1_value + 1:div2_value]
        div3 = img[0:h, div2_value + 1:w]

        cv2.circle(img, (int(w / 2), int(h / 2)), 3, (0, 255, 255), -1)

        # 구분선
        cv2.line(img, (int(w / 3), 0), (int(w / 3), h), (0, 255, 255), 1)
        cv2.line(img, (int(2 * w / 3), 0), (int(2 * w / 3), h), (0, 255, 255), 1)

        # 구분
        cv2.putText(div1, '1', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.putText(div2, '2', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.putText(div3, '3', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)

        gray = cv2.cvtColor(div1, cv2.COLOR_BGR2GRAY)

        # gaussian = cv2.GaussianBlur(gray, (5, 5), 0, 0)
        adaptive_thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 7)

        # _, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

        contour, _ = cv2.findContours(adaptive_thr, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for cont in contour:

            approx = cv2.approxPolyDP(cont, cv2.arcLength(cont, True) * 0.02, True)
            vtc = len(approx)

            if vtc == 4:
                self.setLabel(img, cont, "Rec")

        # cv2.imshow("result", img)
        # cv2.imshow("threshold", adaptive_thr)
        _, jpeg = cv2.imencode('.jpg', img)

        return jpeg.tobytes()


if __name__ == '__main__':
    rr = Rectangle_Recognition()
    while 1:
        rr.stream()
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()