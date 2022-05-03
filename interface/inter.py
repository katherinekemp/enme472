import os
from tkinter import *
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import csv

# Data
water_usage = f"{os.getcwd()}/water_usage.csv"
water_file = open(water_usage)
water_csvreader = csv.reader(water_file)
x_water, y_water = [], []
for row in water_csvreader:
    x_water.append(row[0])
    y_water.append(row[1])

nutrient_usage = f"{os.getcwd()}/nutrient_usage.csv"
nutrient_file = open(nutrient_usage)
nutrient_csvreader = csv.reader(nutrient_file)
x_nutrient, y_nutrient = [], []
for row in nutrient_csvreader:
    x_nutrient.append(row[0])
    y_nutrient.append(row[1])

# Root Window
root = Tk()
root.title("Rotisserie Basil")
screen_height = Tk.winfo_screenheight(root)
screen_width = Tk.winfo_screenwidth(root) 
geometry = f'{screen_width}x{screen_height}'
root.geometry(geometry)



# Column 0: Controls, Updates/Recommendations, Image

# Controls
btn00 = Button(root, text="Refresh")
btn00.place(bordermode=OUTSIDE, anchor='nw', x=50, y=0, height=screen_height//4.5, width=screen_width//2.5)

# Updates/Recommendations
lbl01 = Label(root, text="Updates")
lbl01.place(bordermode=OUTSIDE, anchor='nw', x=50, y=screen_height//4, height=screen_height//4.5, width=screen_width//2.5)

# Image
pathToImage = f"{os.getcwd()}/flower.jpeg"
im = Image.open(pathToImage)
w, h = im.size
width = int(.4 * screen_width)
height = int(h * (width / w))
im = im.resize((width, height))
ph = ImageTk.PhotoImage(im)
lbl2 = Label(root, image=ph)
lbl2.place(bordermode=OUTSIDE, anchor='nw', x=50, y=screen_height//2, height=screen_height//2.5, width=screen_width//2.5)



# Column 1: Water and Nutrient Usage Graphs

# Water Usage Graph
fig1 = Figure(figsize = (5, 5), dpi = 100)

plot1 = fig1.add_subplot()
plot1.plot(x_water, y_water)
plot1.set_title("Water Usage Over Last Week")
plot1.set_xlabel("Time")
plot1.set_ylabel("Height")

canvas1 = FigureCanvasTkAgg(fig1, master=root)  
canvas1.draw()
canvas1.get_tk_widget().place(bordermode=OUTSIDE, anchor='ne', x=screen_width-50, y=40, height=screen_height//2.5, width=screen_width//2.5)

toolbar1 = NavigationToolbar2Tk(canvas1, root)
toolbar1.update()
toolbar1.place(bordermode=OUTSIDE, anchor='ne', x=screen_width-50, y=0)

# Nutrient Usage Graph
fig2 = Figure(figsize = (5, 5), dpi = 100)

plot2 = fig2.add_subplot()
plot2.plot(x_nutrient, y_nutrient)
plot2.set_title("Nutrient Usage Over Last Week")
plot2.set_xlabel("Time")
plot2.set_ylabel("Height")
plot2.locator_params(axis='y', nbins=6)
plot2.locator_params(axis='x', nbins=10)

canvas2 = FigureCanvasTkAgg(fig2, master=root)  
canvas2.draw()
canvas2.get_tk_widget().place(bordermode=OUTSIDE, anchor='ne', x=screen_width-50, y=screen_height//2, height=screen_height//2.5, width=screen_width//2.5)

toolbar2 = NavigationToolbar2Tk(canvas2, root)
toolbar2.update()
toolbar2.place(bordermode=OUTSIDE, anchor='ne', x=screen_width-50, y=screen_height//2-40)



# Main Loop
root.mainloop()
