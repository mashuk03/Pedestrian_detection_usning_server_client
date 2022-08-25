"""
Server start before client
When server receive a request Result, it take a input image from the image directory and run the detect_buoy function on the input image
We expect a camera in the server side. As there is no available camera we take input image from a file directory and read the input image
in the server side.

Once the detect_buoy function save the detection result server send the resultant image to client

"""

import io, os
import socket
import cv2
import sys
import numpy as np
sys.path.append('../BuoyDetection')

from PedDetect import ped_detect
from EKFTracking import EKFTracker

COLORS = [(0, 255, 255), (0, 140, 255), (0, 255, 0)]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 4001))  # bind host address and port together

server.listen()

BUFFER_SIZE = 4096 # set the buffer size
count = 0
while True:
    client_socket, _ = server.accept()
    file_stream = io.BytesIO()

    recv_data = client_socket.recv(BUFFER_SIZE)
    # print(recv_data)

    if recv_data == b"Result" and count < 1:

        img_rgb = cv2.imread("../data/PedImg/00219.jpg")  # read input image from server
        trakers = [EKFTracker(), EKFTracker(), EKFTracker()]
        time = 0
        #### Call the detector here###############

        img_rgb = ped_detect(img_rgb)
        cv2.imwrite('detected_result.jpg', img_rgb)

        with open('detected_result.jpg', 'rb') as file:
            file_data = file.read(BUFFER_SIZE)

            # print(file_data)
            while file_data:
                client_socket.send(file_data)
                file_data = file.read(BUFFER_SIZE)

            count += 1

    client_socket.send(b"%Hello%")
    os.unlink('detected_result.jpg')
    print("Result sent")
    break
