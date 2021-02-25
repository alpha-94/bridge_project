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
        self.text = ''
        self.base_height = 0

    @staticmethod
    def roi(name: str, img, width, height, spot: tuple, clr: str):
        color = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
        }
        x, y = spot
        div = img[y:y + height, x:x + width]

        pt1 = spot
        pt2 = (x + width, y + height)
        # cv2.rectangle(img, pt1, pt2, color[clr], 2)
        cv2.putText(img, name, (pt1[0], pt1[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color[clr], 1)
        cv2.circle(img, (x, y), 3, color[clr], -1)
        return div

    @staticmethod
    def setLabel(img, pts, move_point):
        (x, y, w, h) = cv2.boundingRect(pts)
        pt1 = (x + move_point[0], y + move_point[1])
        pt2 = (x + w + move_point[0], y + h + move_point[1])

        if 94 > h > 30 and 113 > w > 90:
            # print("x :: {}, y :: {}, w :: {}, h :: {}".format(x, y, w, h))
            cv2.rectangle(img, pt1, pt2, (0, 255, 255), 2)
            # print(rec.shape)
            cv2.putText(img, 'w :: {}, h :: {}  safe'.format(w, h), (pt1[0], pt1[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255))
            return 'safe'

        elif 30 > h > 0 and 113 > w > 90:
            # print("x :: {}, y :: {}, w :: {}, h :: {}".format(x, y, w, h))
            cv2.rectangle(img, pt1, pt2, (0, 0, 255), 2)
            # print(rec.shape)
            cv2.putText(img, 'w :: {}, h :: {}  danger'.format(w, h), (pt1[0], pt1[1] - 3), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255))
            return 'danger'

        else:
            return 'None'

    def cleared_setLabel(self, img, pts, move_point):
        (x, y, w, h) = cv2.boundingRect(pts)
        pt1 = (x + move_point[0], y + move_point[1])
        pt2 = (x + move_point[0], y + h + move_point[1])

        if 94 > h > 30 and 113 > w > 90:
            if self.base_height == 0:
                self.base_height = h
            elif self.base_height - h < 0:
                self.base_height = h
            cv2.line(img, pt1, pt2, (0, 255, 255), 2)
            cv2.putText(img, 'h :: {} safe'.format(self.base_height - h), (pt1[0] + 2, pt1[1] + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255), 2)
            return 'safe'

        elif 30 > h > 0 and 113 > w > 90:
            cv2.line(img, pt1, pt2, (0, 0, 255), 2)
            cv2.putText(img, 'h :: {} danger'.format(self.base_height - h), (pt1[0] + 2, pt1[1] + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255), 2)
            return 'danger'

        else:
            return 'None'

    def detective(self, img, size, spot, clr):
        roi = self.roi("{} zone".format(clr), img, size[0], size[1], spot, clr)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # gaussian = cv2.GaussianBlur(gray, (5, 5), 0, 0)
        adaptive_thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 7)

        # _, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

        contour, _ = cv2.findContours(adaptive_thr, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for cont in contour:
            if cv2.contourArea(cont) < 100:  # 노이즈 제거, 너무 작으면 무시
                continue
            approx = cv2.approxPolyDP(cont, cv2.arcLength(cont, True) * 0.02, True)
            vtc = len(approx)

            if vtc == 4:
                state = self.cleared_setLabel(img, cont, spot)
                return adaptive_thr, state
        return adaptive_thr, 'None'

    def stream(self):
        img = self.cap.read()
        img = cv2.resize(img, dsize=(640, 480), interpolation=cv2.INTER_AREA)
        h, w, _ = img.shape

        rec_size = (130, 110)

        clr1 = 'blue'
        spot1 = (250, 220)

        clr2 = 'green'
        spot2 = (250, 116)

        clr3 = 'red'
        spot3 = (250, 18)

        adaptive_thr1, state1 = self.detective(img, rec_size, spot1, clr1)
        if state1 != 'None':
            # cv2.imshow("threshold1", adaptive_thr1)
            self.text = clr1 + ' zone ' + state1
            _, jpeg = cv2.imencode('.jpg', img)
            return jpeg.tobytes(), self.text
        else:
            adaptive_thr2, state2 = self.detective(img, rec_size, spot2, clr2)
            if state2 != 'None':
                # cv2.imshow("threshold2", adaptive_thr1)
                self.text = clr2 + ' zone ' + state2
                _, jpeg = cv2.imencode('.jpg', img)
                return jpeg.tobytes(), self.text
            else:
                adaptive_thr3, state3 = self.detective(img, rec_size, spot3, clr3)
                if state3 != 'None':
                    # cv2.imshow("threshold3", adaptive_thr1)
                    self.text = clr3 + ' zone ' + state3
                    _, jpeg = cv2.imencode('.jpg', img)
                    return jpeg.tobytes(), self.text
                else:
                    cv2.putText(img, 'Not Searching Object', (int(w / 2) - 100, int(h / 2)), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), thickness=2)
                    self.text = 'Not Searching Object'
                    _, jpeg = cv2.imencode('.jpg', img)
                    return jpeg.tobytes(), self.text

        # cv2.imshow("result", img)

        # _, jpeg = cv2.imencode('.jpg', img)
        # return jpeg.tobytes()


if __name__ == '__main__':
    rr = Rectangle_Recognition()
    while 1:
        rr.stream()
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

'''
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
'''
