from skimage import measure, color, filters, metrics
import cv2
from imutils.video import VideoStream
import time
import math
import numpy as np


class Object_Recognition:
    def __init__(self):

        self.cap = VideoStream('test2.mp4').start()
        self.text = ''
        self.base_height = 0

        self.base_image = None
        self.base_roi = None

        self.color = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0),
            'black': (0, 0, 0),
        }

        # cap read 한 image 의 높이, 폭
        self.img_w = 0
        self.img_h = 0

        # roi init
        self.spot = (110, 118)

    def roi_(self, image: np.ndarray, name: str = '', clr: str = 'black',
             is_draw: bool = False):
        """
        :param image: 원본 이미지 입력
        :param name: 영역의 이름을 지정
        :param clr: 색상 지정
        :param is_draw: roi 영역을 표시할지 설정
        :return: 분할 된 영역 이미지 출력
        """

        x, y = self.spot
        div = image[y: y + self.img_h, x: x + self.img_w]

        if is_draw:
            pt1 = self.spot
            pt2 = (x + self.img_w, y + self.img_h)

            cv2.rectangle(image, pt1, pt2, self.color[clr], 2)
            cv2.putText(image, name, (pt1[0], pt1[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color[clr], 1)
            cv2.circle(image, (x, y), 3, self.color[clr], -1)

        return div

    def detective_(self, base_image, compare_image, thr=30, maxval=255):
        """
        :param base_image: 기본 이미지에서 roi 가 된 이미지
        :param compare_image: 비교 할 이미지
        :return: diff 이미지 출력
        :param thr: 임계값
        :param maxval: 임계값 대비 낮으면 0, 높으면 maxval
        """

        diff = cv2.absdiff(base_image, compare_image)
        _, diff = cv2.threshold(diff, thr, maxval, cv2.THRESH_BINARY)

        return diff

    def setLabel_(self, result_image, diff_image, dimension: int = 2):
        """
        :param result_image: 최종 출력 될 이미지
        :param diff_image: 차 영상 이미지
        :param dimension: 1,2,3 차원 지원 / input = 1 | 2 | 3
        """
        if dimension == 1 or 2:
            lines = cv2.HoughLinesP(diff_image, 0.8, np.pi / 180, 90, minLineLength=10, maxLineGap=100)

            for i in lines:
                x, y, w, h = i[0]

                if dimension == 1:
                    cv2.circle(result_image, ((h - x) / 2, (h - y) / 2), 0.3, self.color['blue'], 1)

                elif dimension == 2:
                    cv2.line(result_image, (x, y), (w, h), self.color['red'], 2)

        elif dimension == 3:
            cnt, _, stats, _ = cv2.connectedComponentsWithStats(diff_image)

            for i in range(1, cnt):
                x, y, w, h, s = stats[i]

                if s < 100:
                    continue

                cv2.rectangle(result_image, (x, y, w, h), self.color['red'], 2)

        else:
            print('setLabel ::  dimension 값을 확인 하세요 / dimension :: %d' % dimension)

    def stream_(self):
        image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.base_image is None:
            self.base_image = image
            self.base_roi = self.roi_(self.base_image)
            print('base : ', self.base_image.shape, ' image : ', image.shape)

        self.img_h, self.img_w = image.shape
        compare_image = self.roi_(image)
        print('base : ', self.base_roi.shape, ' image : ', image.shape)

        diff = self.detective_(self.base_roi, compare_image)

        self.setLabel_(image, diff)

        if __name__ == '__main__':
            cv2.imshow('result', image)
            cv2.imshow('diff', diff)

        else:
            self.text = 'complete'
            _, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes(), self.text


if __name__ == '__main__':
    rr = Object_Recognition()
    while 1:
        rr.stream_()
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

'''
        div1_value = int(w / 3)
        div2_value = int(2 * w / 3)

        div1 = image[0:h, 0:div1_value]
        div2 = image[0:h, div1_value + 1:div2_value]
        div3 = image[0:h, div2_value + 1:w]

        cv2.circle(image, (int(w / 2), int(h / 2)), 3, (0, 255, 255), -1)

        # 구분선
        cv2.line(image, (int(w / 3), 0), (int(w / 3), h), (0, 255, 255), 1)
        cv2.line(image, (int(2 * w / 3), 0), (int(2 * w / 3), h), (0, 255, 255), 1)

        # 구분
        cv2.putText(div1, '1', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.putText(div2, '2', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.putText(div3, '3', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
'''
