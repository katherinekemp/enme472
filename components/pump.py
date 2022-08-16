import RPi.GPIO as GPIO          
from time import sleep
from datetime import datetime

# Pins
light = 22 # Pin for light relay control

mp_in1 = 24 # Direction control for main pump 
mp_in2 = 23 # Direction control for main pump
mp_en = 25 # main pump

np_in1 = 17 # nutrients direction 1
np_in2 = 27 # nutrients direction 2
np_en = 18 # nutrients enable


GPIO.setmode(GPIO.BCM) # Chooses board

# Setup output pins for pumps and relays
GPIO.setup(mp_in1,GPIO.OUT)
GPIO.setup(mp_in2,GPIO.OUT)
GPIO.setup(mp_en,GPIO.OUT)
GPIO.setup(light,GPIO.OUT)
GPIO.setup(np_in1,GPIO.OUT)
GPIO.setup(np_in2,GPIO.OUT)
GPIO.setup(np_en,GPIO.OUT)

# intialize output pin states
GPIO.output(light,GPIO.LOW)
GPIO.output(mp_in1,GPIO.HIGH)
GPIO.output(mp_in2,GPIO.LOW)
GPIO.output(np_in1,GPIO.LOW)
GPIO.output(np_in2,GPIO.HIGH)

# Run main pump at normal rate
p=GPIO.PWM(mp_en,500)
p.start(35)

n = GPIO.PWM(np_en,500)
n.start(40)


light_flag = False # initialize light state to off

# Constants
midnight = datetime(1,1,1,23,0,0).time() 
morning = datetime(1,1,1,5,0,0).time()

while (1):
    time = datetime.now().time() # Get current time

    # Set lights to proper staet
    if light_flag == True and (time > midnight or time < morning):
        GPIO.output(light,GPIO.LOW)
        light_flag = False
    elif light_flag == False and not (time > midnight or time < morning):
        GPIO.output(light,GPIO.HIGH)
        light_flag = True

