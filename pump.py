import RPi.GPIO as GPIO          
from time import sleep
from datetime import datetime

# Pins
light = 22 # Pin for light relay control
in1 = 24 # Direction control for main pump 
in2 = 23 # Direction control for main pump
en = 25 # main pump


GPIO.setmode(GPIO.BCM) # Chooses boar

# Setup output pins for pumps and relays
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(light,GPIO.OUT)

# intialize output pin states
GPIO.output(light,GPIO.LOW)
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)

# Run main pump at normal rate
p=GPIO.PWM(en,500)
p.start(35)


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
