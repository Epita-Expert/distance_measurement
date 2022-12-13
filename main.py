from collections import deque
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

def distance_to_camera(focalLength, ballWidth):
    # compute and return the distance from the maker to the camera
    KNOWN_WIDTH = 4.27 * 0.01 * 39.37
    return ((KNOWN_WIDTH * focalLength) / ballWidth) / 39.37

def init_focal_length(marker, knownDistanceMeter):
    # initialize the known distance from the camera to the object, which
    # in this case is 24 inches
    KNOWN_DISTANCE = knownDistanceMeter * 39.37
    # initialize the known object width, which in this case, the piece of
    # paper is 12 inches wide
    KNOWN_WIDTH = 4.27 * 0.01 * 39.37
    # load the furst image that contains an object that is KNOWN TO BE 2 feet
    # from our camera, then find the paper marker in the image, and initialize
    # the focal length
    # image = cv2.imread("images/2ft.png")
    # marker = find_marker(image)
    return ((marker * 2) * KNOWN_DISTANCE) / KNOWN_WIDTH



ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
lower_green = (55, 55, 55)
upper_green = (78, 255, 255)
init = False

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(1)
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

while True:
    (grabbed, frame) = camera.read()
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
	# color space
    frame = imutils.resize(frame, width=900)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    for cnt in cnts:
        c = max(cnts, key=cv2.contourArea)
        area = cv2.contourArea(cnt)

        rect = cv2.minAreaRect(c)

        ((x, y), radius) = cv2.minEnclosingCircle(c)
        print("rect : {0}".format(rect))

        if not init:
            init = True
            focalLength = init_focal_length(radius, 2)
            print("focal length : {0}".format(focalLength))

        if radius < 60:
           cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
           inches = distance_to_camera(focalLength, radius * 2)
           cv2.putText(frame, "Balle - distance: {0}".format(inches), (int(x), int(y)),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
           print("Balle - area: {0}".format(int(area)))
           print("Balle - x: {0}".format(int(x)))
           print("Balle - y: {0}".format(int(y)))
           print("Balle - radius: {0}".format(int(radius)))
           print("center : {0}".format(center))
           print("focal length : {0}".format(focalLength))

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
