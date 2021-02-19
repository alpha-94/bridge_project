import cv2
import math
import numpy as np



def grid(image, step):
    rows, cols, _ = image.shape

    step = step
    x = np.linspace(start=0, stop=rows, num=step)
    y = np.linspace(start=0, stop=cols, num=step)

    v_xy = []
    h_xy = []

    for i in range(step):
        v_xy.append([int(x[i]), 0, int(x[i]), rows - 1])
        h_xy.append([0, int(y[i]), cols - 1, int(y[i])])

    for i in range(step):
        [x1, y1, x2, y2] = v_xy[i]
        [x1_, y1_, x2_, y2_] = h_xy[i]

        cv2.line(image, (x1, y1), (x2, y2), (242, 242, 242), 1)
        cv2.line(image, (x1_, y1_), (x2_, y2_), (242, 242, 242), 1)


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, img = cap.read()
    if img is None:
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 120)
    lines = cv2.HoughLinesP(edges, 1, math.pi / 1, 20, None, 2, 480)

    if lines is None:
        print('No Hough Lines found in image.')
        break
    else:
        dot1 = (lines[0][0][0], lines[0][0][1])
        dot2 = (lines[0][0][2], lines[0][0][3])
        cv2.line(img, dot1, dot2, (255, 0, 0), 3)
        cv2.imshow("output", img)
        length = lines[0][0][1] - lines[0][0][3]
        print(length)
        key = cv2.waitKey(10)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
