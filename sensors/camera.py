from picamera import PiCamera
from time import sleep
import os

'''
camera = PiCamera()
camera.start_preview()
sleep(5)

while 1:
    camera.capture('/tmp/picture.jpg')
    camera.stop_preview()
    sleep(5)
'''

os.system("raspistill -n -o ./data/plant.jpg")
