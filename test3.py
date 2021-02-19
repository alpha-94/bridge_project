# 움직임 물체 찾기

import cv2 as cv
import numpy as np


def main():
    cap = cv.VideoCapture(0)

    bgs = cv.createBackgroundSubtractorKNN(dist2Threshold=500, detectShadows=False)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv.INTER_CUBIC)
        fgmask = bgs.apply(frame)

        cv.imshow('video', frame)
        cv.imshow('moving', fgmask)

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
