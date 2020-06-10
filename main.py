import argparse
import cv2
import numpy as np
import cv2
import imutils

import math

cropping = False
 
x_start, y_start, x_end, y_end = 0, 0, 0, 0

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
 
# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"]) 
oriImage = image.copy()
 
def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping
 
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
 
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
 
    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished
 
        refPoint = [(x_start, y_start), (x_end, y_end)]
 
        if len(refPoint) == 2: #when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped", roi)
            imgC = roi
            imgG = cv2.cvtColor(imgC, cv2.COLOR_BGR2GRAY)
            median = cv2.medianBlur(imgG, 5)

            m = cv2.mean(median)[0]
            Hasil = 0.918183201 + (0.0127839853*m)

            print("Mean Intensity Pupil : {}".format(m))

            if(Hasil > 0 and Hasil < 1.5):
                print("Prediksi : Normal")
            elif (Hasil >= 1.5 and Hasil < 2.5):
                print("Prediksi : Imatur")
            else:
                print("Prediksi : Matur")

 
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)
 
while True:
 
    i = image.copy()
 
    if not cropping:
        cv2.imshow("image", image)
 
    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("image", i)
 
    cv2.waitKey(1)
 
# close all open windows
cv2.destroyAllWindows()
