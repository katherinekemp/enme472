import RPi.GPIO as GPIO          
from time import sleep
from datetime import datetime
from datetime import timedelta
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from picamera import PiCamera

## CAMERA
camera = PiCamera()
camera.start_preview()
sleep(5)

## MOTORS
# Pins
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
GPIO.setup(np_in1,GPIO.OUT)
GPIO.setup(np_in2,GPIO.OUT)
GPIO.setup(np_en,GPIO.OUT)

# intialize output pin states
GPIO.output(mp_in1,GPIO.HIGH)
GPIO.output(mp_in2,GPIO.LOW)
GPIO.output(np_in1,GPIO.LOW)
GPIO.output(np_in2,GPIO.HIGH)

# Run main pump at normal rate
p=GPIO.PWM(mp_en,500) # freq = 500
p.start(35) # 35% duty cycle

n = GPIO.PWM(np_en,500)

## LIGHTS
light = 22 # Pin for light relay control
light_flag = False # initialize light state to off
GPIO.setup(light,GPIO.OUT) # Set pin to output
GPIO.output(light,GPIO.LOW) # Set pin to low

# Constants
MIDNIGHT = datetime(1,1,1,23,0,0).time() 
MORNING = datetime(1,1,1,5,0,0).time()

## CONDUCTIVITY
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
cs = digitalio.DigitalInOut(board.D5) # create the cs (chip select)
mcp = MCP.MCP3008(spi, cs) # create the mcp object
chan = AnalogIn(mcp, MCP.P0) # create an analog input channel on pin 0
NUTRIENT_THRESHOLD = 2.5 # Nutrient constant
last_nutrient_check = datetime.now().time()

## WATER LEVEL
GPIO_TRIGGER = 5 # trigger pin
GPIO_ECHO = 6 # echo pin
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) #set GPIO direction (IN / OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN) #set GPIO direction (IN / OUT)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


while (1):
    time = datetime.now().time() # Get current time

    # Set lights to proper staet
    if light_flag == True and (time > MIDNIGHT or time < MORNING):
        GPIO.output(light,GPIO.LOW)
        light_flag = False
    elif light_flag == False and not (time > MIDNIGHT or time < MORNING):
        GPIO.output(light,GPIO.HIGH)
        light_flag = True

    # Measure conductivity
    nutrient_level = chan.voltage
    print('ADC Voltage: ' + str(chan.voltage) + 'V')
    if ((time - last_nutrient_check > timedelta(minutes=2)) and (nutrient_level < NUTRIENT_THRESHOLD)):
        n.start(40)
        sleep(1)
        n.stop()
        last_nutrient_check = time

    # Get water level
    water_level = distance()
    print (f"Measured Distance = {water_level} cm")
    
    # Capture Image
    camera.capture('./plants.jpg')
    camera.stop_preview()

    # Pause
    sleep(1)