import os
import cv2
import time

def saveVideoFrame(frame, input_file, output_file):
    vid = cv2.VideoCapture(input_file)

    success, image = vid.read()
    count = 0
    while success:
        sucess, image = vid.read()

        if count == frame:
            cv2.imwrite(output_file, image)
            break

        count += 1
