from telegram_message import send_warning, send_message
import cv2
from ultralytics import YOLO
import numpy as np
import time
import pyglet

model = YOLO(r"Model\best.pt")
COLOR = (0,0,255)
start_time , end_time = -100 , 0
#read frame from camera
cam = cv2.VideoCapture(0)

while True:
    #check
    check = False
    # read img from camera real time
    _, img = cam.read()
    # predict
    result = model.predict( source= img, imgsz= 640, stream= False , save= False , conf= 0.6)
    # draw boxes
    for r in result:
        boxes = r.boxes
        for box in boxes:
            check = True
            left, top, right, bottom = np.array(box.xyxy.cpu(), dtype=np.int64 ).squeeze()
            cv2.rectangle(img, (left, top),(right, bottom), COLOR, 2)
    # show real time
    cv2.imshow('image', img)
    #send warning
    end_time = time.time()
    if check and (end_time - start_time) >= 60 :
        start_time = time.time()
        cv2.imwrite('warning.png', img)
        # Play file sound
        music = pyglet.resource.media('police.wav')
        music.play()
        #pyglet.app.run()
        send_warning(img_path= 'warning.png')
        send_message()
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyWindow()
