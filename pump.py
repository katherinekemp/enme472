import RPi.GPIO as GPIO          
from time import sleep

in1 = 24
in2 = 23
en = 25
light = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(light,GPIO.OUT)
GPIO.output(light,GPIO.LOW)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,500)
p.start(80)

while (1):
    GPIO.output(in1,GPIO.LOW)
    sleep(20)
    GPIO.output(in1,GPIO.HIGH)
    sleep(20)