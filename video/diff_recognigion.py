from skimage import measure, color, filters, metrics

from imutils.video import VideoStream
import cv2
import time
import math


class Diff_Recognition:
    def __init__(self):
        self.cap = VideoStream('rtsp://10.0.0.97:554/main&media=video&media=audio').start()

        img_base = self.cap.read()
        img_base = cv2.resize(img_base, dsize=(576, 324), interpolation=cv2.INTER_AREA)
        self.img_base = cv2.cvtColor(img_base, cv2.COLOR_BGR2GRAY)

        self.count = 0
        self.score = 0
        self.custom = 50

    def stream(self):
        img_result = self.cap.read()
        try:
            img_result = cv2.resize(img_result, dsize=(576, 324), interpolation=cv2.INTER_AREA)
            img = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)

            self.count += 1
            if self.count > self.custom:
                (self.score, diff_) = metrics.structural_similarity(self.img_base, img, full=True)
                diff = (diff_ * 255).astype("uint8")
                print("count :: {}  // ssim :: {}".format(self.count, self.score))

                self.count = 0

            cv2.putText(img_result, str(int(self.score * 100)), (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 1)
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
