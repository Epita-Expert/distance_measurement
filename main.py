from collections import deque
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

# Balle Jaune: 6.7
# sizeBall = 6.7
# lower_green = (18, 210, 20)
# upper_green = (30, 255, 255)

# config balle verte
# sizeBall = 2.3
# lower_green = (36, 69, 20)
# upper_green = (75, 255, 255)

# config balle de golf sous l'eau
# sizeBall = 4.27
# lower_green = (55, 0, 20)
# upper_green = (80, 255, 255)

# config balle de tenis
sizeBall = 6.6
lower_green = (30, 50, 50)
upper_green = (50, 255, 255)

## config balle orange
# NOT FOUND !!!!!!!!!!!
# lower_green = (10, 180, 20)
# upper_green = (15, 190, 255)
# NOT FOUND !!!!!!!!!!!

def distance_to_camera(focalLength, ballWidth):
    # compute and return the distance from the maker to the camera
    KNOWN_WIDTH = sizeBall * 0.01
    return ((KNOWN_WIDTH * focalLength) / ballWidth)

def init_focal_length(radius, knownDistanceMeter):
    # initialize the known distance from the camera to the object, which
    # in this case is 1 or 2 meters
    KNOWN_DISTANCE = knownDistanceMeter
    # initialize the known object width, which in this case, the piece of
    # paper is 2.7 cm wide
    KNOWN_WIDTH = sizeBall * 0.01
    # load the first image that contains an object that is KNOWN TO BE 1 or 2 meters
    # from our camera, then find the paper marker in the image, and initialize
    # the focal length
    return ((radius * 2) * KNOWN_DISTANCE) / KNOWN_WIDTH

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

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

        if not init:
            init = True
            focalLength = init_focal_length(radius, 1)

        if radius < 120:
           cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
           inches = round(distance_to_camera(focalLength, radius * 2), 2)
           cv2.putText(frame, "Balle - distance: {0}".format(inches), (int(x), int(y)),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 150, 0))
           print("inches : {0}".format(inches))

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
