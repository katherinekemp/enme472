import RPi.GPIO as GPIO          
from time import sleep
from datetime import datetime

# Pins
light = 22 # Pin for light relay control
in1 = 24 # Direction control for main pump 
in2 = 23 # Direction control for main pump
en = 25 # main pump
n1 = 17 # nutrients direction 1
n2 = 27 # nutrients direction 2
nen = 18 # nutrients enable


GPIO.setmode(GPIO.BCM) # Chooses boar

# Setup output pins for pumps and relays
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(light,GPIO.OUT)
GPIO.setup(n1,GPIO.OUT)
GPIO.setup(n2,GPIO.OUT)
GPIO.setup(nen,GPIO.OUT)

# intialize output pin states
GPIO.output(light,GPIO.LOW)
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)
GPIO.output(n1,GPIO.LOW)
GPIO.output(n2,GPIO.HIGH)

# Run main pump at normal rate
p=GPIO.PWM(en,500)
p.start(35)

n = GPIO.PWM(nen,500)
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

