import os
from tkinter import *
from PIL import Image, ImageTk
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import sqldb
import RPi.GPIO as GPIO          
from time import sleep
import time
from datetime import datetime
from datetime import timedelta
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from send_text import send_text

# LOCATIONS
data_folder = "data"

## MOTORS
# Pins
mp_in1 = 24 # Direction control for main pump 
mp_in2 = 23 # Direction control for main pump
mp_en = 25 # main pump

np_in1 = 17 # nutrients direction 1
np_in2 = 27 # nutrients direction 2
np_en = 18 # nutrients enable

## LIGHTS
light = 22 # Pin for light relay control
light_flag = False # initialize light state to off
MIDNIGHT = datetime(1,1,1,23,0,0).time() # nightimte constant
MORNING = datetime(1,1,1,5,0,0).time() # morning constant

## CONDUCTIVITY
NUTRIENT_THRESHOLD_SEEDLING = 0.66 # Nutrient constant for seedling
NUTRIENT_THRESHOLD_YOUNG = 0.82 # Nutrient constant for young plants
NUTRIENT_THRESHOLD_MATURE = 1.02 # Nutrient constant for fully grown plants
last_nutrient_check = datetime.now().time()
conductivity_power = 16 # Power to analog chip

## WATER LEVEL
GPIO_TRIGGER = 5 # trigger pin
GPIO_ECHO = 6 # echo pin
WATER_LEVEL_LOW = 7 # cm
WATER_LEVEL_THRESHOLD = 5 # cm
SONAR_HEIGHT = 21 # cm
water_low_counter = 0
water_threshold_counter = 0


## SET UP
def set_up():
    global mp_in1, mp_in2, mp_en, np_in1, np_in2, np_en, light, GPIO_TRIGGER, GPIO_ECHO, chan, n, p
    print("SETUP")
    
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

    # MAIN PUMP
    p=GPIO.PWM(mp_en,500) # freq = 500
    p.start(35) # 35% duty cycle

    # NUTRIENT PUMP
    n = GPIO.PWM(np_en,500)

    ## LIGHTS
    GPIO.setup(light,GPIO.OUT) # Set pin to output
    GPIO.output(light,GPIO.LOW) # Set pin to low

    ## CONDUCTIVITY
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
    cs = digitalio.DigitalInOut(board.D5) # create the cs (chip select)
    mcp = MCP.MCP3008(spi, cs) # create the mcp object
    chan = AnalogIn(mcp, MCP.P0) # create an analog input channel on pin 0
    GPIO.setup(conductivity_power,GPIO.OUT)
    GPIO.output(conductivity_power,GPIO.HIGH)

    ## WATER LEVEL
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT) #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN) #set GPIO direction (IN / OUT)

    ## IMAGE
    os.system("raspistill -n -o ./data/plant.jpg")

## ADD TIME
def time_plus(current_time, timedelta):
    start = datetime(
        2000, 1, 1,
        hour=current_time.hour, minute=current_time.minute, second=current_time.second)
    end = start + timedelta
    return end.time()


def distance():
    global GPIO_TRIGGER, GPIO_ECHO

    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    sleep(0.00001)
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


def run_system():
    global light_flag, MIDNIGHT, MORNING, light, chan, n, last_nutrient_check, NUTRIENT_THRESHOLD_SEEDLING, SONAR_HEIGHT, WATER_LEVEL_THRESHOLD, WATER_LEVEL_LOW, water_threshold_counter, water_low_counter
    current_time = datetime.now() # Get current time

    ## LIGHTS
    if light_flag == True and (current_time.time() > MIDNIGHT or current_time.time() < MORNING):
        GPIO.output(light,GPIO.LOW)
        light_flag = False
    elif light_flag == False and not (current_time.time() > MIDNIGHT or current_time.time() < MORNING):
        GPIO.output(light,GPIO.HIGH)
        light_flag = True

    # CONDUCTIVITY
    #GPIO.output(conductivity_power,GPIO.HIGH)
    #sleep(5)
    nutrient_level = chan.voltage
    #sleep(5)
    #GPIO.output(conductivity_power,GPIO.LOW)
    x1, y1 = .45, 0
    x2, y2 = 1.05, 2500
    slope = (y2 - y1) / (x2 - x1)
    nutrient_level_ppm = y1 + slope * (nutrient_level - x1) 
    sqldb.save_sql_data(nutrient_usage_path, [current_time.timestamp()], [nutrient_level_ppm])
    print('ADC Voltage: ' + str(chan.voltage) + 'V')

    if ((current_time.time() > time_plus(last_nutrient_check, timedelta(minutes=2))) and (nutrient_level < NUTRIENT_THRESHOLD_SEEDLING)):
        n.start(40)
        sleep(.2)
        n.stop()
        last_nutrient_check = current_time.time()

    # Get water level
    water_level = SONAR_HEIGHT - distance()
    sqldb.save_sql_data(water_usage_path, [current_time.timestamp()], [water_level])
    print (f"Measured Distance = {water_level} cm")

    if water_level > WATER_LEVEL_LOW:
        water_low_counter = 0
    if water_level > WATER_LEVEL_THRESHOLD:
        water_threshold_counter = 0
        
    if water_level < WATER_LEVEL_THRESHOLD:
        water_threshold_counter += 1
        if water_threshold_counter == 5:
            send_text("Your plants are going to die! The water is below 5 cm. Change it soon.")
            print("CHANGE THE WATER")
    elif water_level < WATER_LEVEL_LOW:
        water_low_counter += 1
        if water_low_counter == 5:
            send_text("Your plants are in danger! The water is between 5 and 7 cm. Consider refilling it soon.")
            print("WATER LEVEL LOW")        

    # Capture Image
    os.system("raspistill -n -o ./data/plant.jpg")

# Data
data_folder = "data"
water_usage_path = f"{os.getcwd()}/{data_folder}/water_usage.db"
nutrient_usage_path = f"{os.getcwd()}/{data_folder}/nutrient_usage.db"

def update_data():
    global x_water, y_water, x_nutrient, y_nutrient
    
    water_usage = sqldb.get_sql_data(water_usage_path)
    nutrient_usage = sqldb.get_sql_data(nutrient_usage_path)
    x_water, y_water, x_nutrient, y_nutrient =  water_usage[0], water_usage[1], nutrient_usage[0], nutrient_usage[1]
    x_water = [datetime.fromtimestamp(x) for x in x_water]
    y_water = [(y if y > 0 else 0) for y in y_water]
    x_temp, y_temp = [], []
    for i in range(len(x_water)):
        if datetime.now().timestamp() - x_water[i].timestamp() <= 6 * 3600:
            x_temp.append(x_water[i])
            y_temp.append(y_water[i])
 
    x_water = x_temp
    y_water = y_temp
                   
    x_nutrient = [datetime.fromtimestamp(x) for x in x_nutrient]
    y_nutrient = [(y if y > 0 else 0) for y in y_nutrient]
    x_temp, y_temp = [], []
    for i in range(len(x_nutrient)):
        if datetime.now().timestamp() - x_nutrient[i].timestamp() <= 6 * 3600: 
            x_temp.append(x_nutrient[i])
            y_temp.append(y_nutrient[i])

    x_nutrient = x_temp
    y_nutrient = y_temp

update_data()

# Root Window
root = Tk()
root.title("Rotisserie Basil")
screen_height = Tk.winfo_screenheight(root)
screen_width = Tk.winfo_screenwidth(root) 
geometry = f'{screen_width}x{screen_height}'
root.geometry(geometry)



# Column 0: Controls, Updates/Recommendations, Image

# Updates/Recommendations
lbl00 = Label(root, text=f"Updates:", font=("Helvetica", 70), fg='#f00')
lbl00.place(bordermode=OUTSIDE, anchor='nw', x=50, y=0, height=screen_height//10, width=screen_width//2)

c = "--" if len(y_water) == 0 else int(y_water[-1]*10)/10
lbl01 = Label(root, text=f"Water height is {c} cm", font=("Helvetica", 36))
lbl01.place(bordermode=OUTSIDE, anchor='nw', x=50, y=screen_height//10, height=screen_height//10, width=screen_width//2)

lbl02 = Label(root, text=f"Water needs to be changed below 5 cm", font=("Helvetica", 36), fg='#696969')
lbl02.place(bordermode=OUTSIDE, anchor='nw', x=50, y=screen_height//5, height=screen_height//10, width=screen_width//2)

c = "--" if len(y_nutrient) == 0 else int(y_nutrient[-1])
lbl03 = Label(root, text=f"Nutrient concentration is {c} ppm", font=("Helvetica", 36))
lbl03.place(bordermode=OUTSIDE, anchor='nw', x=50, y=3*screen_height//10, height=screen_height//10, width=screen_width//2)

lbl04 = Label(root, text=f"Desired nutrient concentration is 625 ppm", font=("Helvetica", 36), fg='#696969')
lbl04.place(bordermode=OUTSIDE, anchor='nw', x=50, y=2*screen_height//5, height=screen_height//10, width=screen_width//2)

# Image
def draw_image():
    global im, screen_width, ph, lbl06, root, screen_height
    
    pathToImage = f"{os.getcwd()}/{data_folder}/plant.jpg"
    im = Image.open(pathToImage)
    w, h = im.size
    width = int(.4 * screen_width)
    height = int(h * (width / w))
    im = im.resize((width, height))
    ph = ImageTk.PhotoImage(im)
    lbl06 = Label(root, image=ph)
    lbl06.place(bordermode=OUTSIDE, anchor='nw', x=150, y=screen_height//2, height=screen_height//2.5, width=screen_width//2.5)

draw_image()

# Date formatter
formatter = mdates.DateFormatter("%H:%M")

# Column 1: Water and Nutrient Usage Graphs

# Water Usage Graph
def draw_water_graph():
    global fig1, plot1, canvas1, toolbar1, formatter
     
    fig1 = Figure(figsize = (5, 5), dpi = 100)

    plot1 = fig1.add_subplot()
    plot1.plot(x_water, y_water)
    plot1.set_title("Water Usage")
    plot1.set_xlabel("Time")
    plot1.set_ylabel("Height (cm)")
    plot1.xaxis.set_major_formatter(formatter)
    
    canvas1 = FigureCanvasTkAgg(fig1, master=root)  
    canvas1.draw()
    canvas1.get_tk_widget().place(bordermode=OUTSIDE, anchor='ne', x=screen_width-50, y=40, height=screen_height//2.5, width=screen_width//2.5)

    toolbar1 = NavigationToolbar2Tk(canvas1, root)
    toolbar1.update()
    toolbar1.place(bordermode=OUTSIDE, anchor='ne', x=screen_width-50, y=0)

draw_water_graph()

# Nutrient Usage Graph
def draw_nutrient_graph():
    global fig2, plot2, canvas2, toolbar2, formatter
    
    fig2 = Figure(figsize = (5, 5), dpi = 100)

    plot2 = fig2.add_subplot()
    plot2.plot(x_nutrient, y_nutrient)
    plot2.set_title("Nutrient Usage")
    plot2.set_xlabel("Time")
    plot2.set_ylabel("Concentration (ppm)")
    plot2.xaxis.set_major_formatter(formatter)
    
    canvas2 = FigureCanvasTkAgg(fig2, master=root)  
    canvas2.draw()
    canvas2.get_tk_widget().place(bordermode=OUTSIDE, anchor='ne', x=screen_width-50, y=screen_height//2, height=screen_height//2.5, width=screen_width//2.5)

    toolbar2 = NavigationToolbar2Tk(canvas2, root)
    toolbar2.update()
    toolbar2.place(bordermode=OUTSIDE, anchor='ne', x=screen_width-50, y=screen_height//2-40)

draw_nutrient_graph()

def update_screen():
    global root, lbl01, y_water, screen_width, screen_height
    
    run_system() # Take measurements
    update_data() # Retrieve data

    # Updates
    c = "--" if len(y_water) == 0 else int(y_water[-1]*10)/10
    lbl01.config(text=f"Water height is {c} cm")

    c = "--" if len(y_nutrient) == 0 else int(y_nutrient[-1])
    lbl03.config(text=f"Nutrient concentration is {c} ppm")
    
    # Image
    draw_image()

    # Graphs
    draw_water_graph()
    draw_nutrient_graph()
    root.after(1000, update_screen)

# Main Loop
set_up()
root.after(1000, update_screen)
root.mainloop()

