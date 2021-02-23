from skimage import measure, color, filters, metrics

from imutils.video import VideoStream
import cv2


class Clean_Video:
    def __init__(self):
        self.cap = VideoStream('rtsp://10.0.0.97:554/main&media=video&media=audio').start()

    def stream(self):
        img = self.cap.read()
        img = cv2.resize(img, dsize=(576, 324), interpolation=cv2.INTER_AREA)

        _, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

        # cv2.imshow("clean", img)


if __name__ == '__main__':
    dr = Clean_Video()
    while 1:
        dr.stream()
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
