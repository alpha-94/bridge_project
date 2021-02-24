from skimage import measure, color, filters, metrics

from imutils.video import VideoStream
import cv2
import imutils
import time
import math


class Diff_Recognition:
    def __init__(self):
        self.cap = VideoStream('rtsp://10.0.0.97:554/main&media=video&media=audio').start()

        # based image
        img_base = self.cap.read()
        img_base = cv2.resize(img_base, dsize=(576, 324), interpolation=cv2.INTER_AREA)
        h, w, _ = img_base.shape

        div1_value_ = int(w / 3)
        div2_value_ = int(2 * w / 3)

        div1 = img_base[0:h, 0:div1_value_]
        div2 = img_base[0:h, div1_value_ + 1:div2_value_]
        div3 = img_base[0:h, div2_value_ + 1:w]

        self.img_base = cv2.cvtColor(div1, cv2.COLOR_BGR2GRAY)

        # diff param
        self.count = 0
        self.score = 0
        self.custom = 50
        self.diff = None

        # background MOG2
        self.backSub = cv2.createBackgroundSubtractorMOG2()

    def stream(self):
        img_result = self.cap.read()

        try:
            img_result = cv2.resize(img_result, dsize=(576, 324), interpolation=cv2.INTER_AREA)
            h, w, _ = img_result.shape

            div1_value = int(w / 3)
            div2_value = int(2 * w / 3)

            div1 = img_result[0:h, 0:div1_value]
            div2 = img_result[0:h, div1_value + 1:div2_value]
            div3 = img_result[0:h, div2_value + 1:w]

            cv2.circle(img_result, (int(w / 2), int(h / 2)), 3, (0, 255, 255), -1)

            # 구분선
            cv2.line(img_result, (int(w / 3), 0), (int(w / 3), h), (0, 255, 255), 1)
            cv2.line(img_result, (int(2 * w / 3), 0), (int(2 * w / 3), h), (0, 255, 255), 1)

            # 구분
            cv2.putText(div1, '1', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
            cv2.putText(div2, '2', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
            cv2.putText(div3, '3', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)

            img = cv2.cvtColor(div1, cv2.COLOR_BGR2GRAY)

            self.count += 1
            if self.count > self.custom:
                (self.score, diff) = metrics.structural_similarity(self.img_base, img, full=True)
                self.diff = (diff * 255).astype("uint8")
                print("count :: {}  // ssim :: {}".format(self.count, self.score))

                self.count = 0

            if self.diff is not None:
                thresh = cv2.threshold(self.diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)

                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(img_result, (x, y), (x + w, y + h), (0, 0, 255), 3)

                cv2.imshow("diff", self.diff)

            cv2.putText(img_result, str(int(self.score * 100)), (30, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
            # cv2.imshow("rr", img_result)

        except cv2.error as e:
            print(e)
            self.__init__()

        _, jpeg = cv2.imencode('.jpg', img_result)

        return jpeg.tobytes()

        # cv2.imshow("dr", img_result)


if __name__ == '__main__':
    dr = Diff_Recognition()
    while 1:
        dr.stream()
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
