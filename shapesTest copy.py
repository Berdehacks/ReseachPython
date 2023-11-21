import cv2
import numpy as np
from matplotlib import pyplot as plt

# reading image
img = cv2.imread('1.jpg')


# r = cv2.selectROI("ROI", img)
# img = img[int(r[1]):int(r[1]+r[3]),  int(r[0]):int(r[0]+r[2])]

# converting image into grayscale imag
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# setting threshold of gray image
_, threshold = cv2.threshold(gray, 140, 180, cv2.THRESH_BINARY)

threshold = cv2.bitwise_not(threshold)

kernel = np.ones((2, 2), np.uint8)
kernel1 = np.ones((1, 1), np.uint8)

opened = cv2.erode(threshold, kernel, iterations=7)
# opened = cv2.dilate(threshold, kernel, iterations=2)
# opened = cv2.erode(threshold, kernel, iterations=4)


plt.imshow(threshold, 'gray')
plt.show()


# using a findContours() function
contours, _ = cv2.findContours(
    opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# list for storing names of shapes
for contour in contours[1:]:
    # cv2.approxPloyDP() function to approximate the shape
    approx = cv2.approxPolyDP(
        contour, 0.05 * cv2.arcLength(contour, True), True)

    # using drawContours() function

    # finding center point of shape
    M = cv2.moments(contour)
    if M['m00'] != 0.0:
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])

    # putting shape name at center of each shape
    if len(approx) == 3:
        # cv2.putText(img, 'Triangle', (x, y),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        pass

    elif len(approx) == 4:
        # cv2.putText(img, 'Quadrilateral', (x, y),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        pass

    elif len(approx) == 5:
        # cv2.putText(img, 'Pentagon', (x, y),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        # # DAVID, los valores de X y Y ya se dan aqui con respecto a toda la imagen``
        # cv2.circle(img, (x, y), 7, (0, 0, 255), -1)
        # cv2.drawContours(img, [contour], 0, (0, 255, 255), 5)
        pass

    elif len(approx) == 6:

        # DAVID, los valores de X y Y ya se dan aqui con respecto a toda la imagen
        cv2.circle(img, (x, y), 7, (0, 0, 255), -1)
        cv2.putText(img, 'Hexagon', (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.drawContours(img, [contour], 0, (0, 255, 255), 5)
        # pass

    else:
        cv2.putText(img, 'circle', (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


# displaying the image after drawing contours
cv2.imshow('shapes', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
