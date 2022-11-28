import cv2
import numpy as np


def nothing(x):
    pass


# define a video capture object
vid = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)
cv2.createTrackbar('L-H', 'Trackbars', 16, 180, nothing)
cv2.createTrackbar('L-S', 'Trackbars', 56, 255, nothing)
cv2.createTrackbar('L-V', 'Trackbars', 94, 255, nothing)
cv2.createTrackbar('U-H', 'Trackbars', 100, 180, nothing)
cv2.createTrackbar('U-S', 'Trackbars', 178, 255, nothing)
cv2.createTrackbar('U-V', 'Trackbars', 255, 255, nothing)


while(True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos('L-H', 'Trackbars')
    l_s = cv2.getTrackbarPos('L-S', 'Trackbars')
    l_v = cv2.getTrackbarPos('L-V', 'Trackbars')
    u_h = cv2.getTrackbarPos('U-H', 'Trackbars')
    u_s = cv2.getTrackbarPos('U-S', 'Trackbars')
    u_v = cv2.getTrackbarPos('U-V', 'Trackbars')

    lower_red = np.array([l_h, l_s, l_v])  # 0,0,0
    upper_red = np.array([u_h, u_s, u_v])  # 180,255,255

    mask = cv2.inRange(hsv, lower_red, upper_red)

    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.erode(mask, kernel, iterations=1)

    # Contours detection

    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if area > 400:
            print(area)
            # print(len(approx))
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 2)
            if len(approx) >= 12 and len(approx) <= 19:
                cv2.putText(frame, "Balle - distance: {0}".format(area), (x, y),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

    # Display the resulting frame
    cv2.imshow('mask', mask)
    cv2.imshow('frame', frame)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
