import busio
import RPi.GPIO as GPIO
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep

# PIN 16 ON/OFF FOR CONDUCTIVITY
nutrient_sense = 16
GPIO.setmode(GPIO.BCM)

GPIO.setup(nutrient_sense,GPIO.OUT)
GPIO.output(nutrient_sense, GPIO.HIGH)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

while (1):
    print('Raw ADC Value: ', chan.value)
    print('ADC Voltage: ' + str(chan.voltage) + 'V')
    sleep(1)
