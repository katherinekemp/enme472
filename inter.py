import os
from tkinter import *
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import sqldb
#import system

# Data
data_folder = "data"
water_usage_path = f"{os.getcwd()}/{data_folder}/water_usage.db"
nutrient_usage_path = f"{os.getcwd()}/{data_folder}/nutrient_usage.db"

def update_data():
    water_usage = sqldb.get_sql_data(water_usage_path)
    nutrient_usage = sqldb.get_sql_data(nutrient_usage_path)
    return water_usage[0], water_usage[1], nutrient_usage[0], nutrient_usage[1]

    # PROCESS DATA FOR ONLY MOST RECENT

x_water, y_water, x_nutrient, y_nutrient = update_data()

# Root Window
root = Tk()
root.title("Rotisserie Basil")
screen_height = Tk.winfo_screenheight(root)
screen_width = Tk.winfo_screenwidth(root) 
geometry = f'{screen_width}x{screen_height}'
root.geometry(geometry)



# Column 0: Controls, Updates/Recommendations, Image

# Updates/Recommendations
lbl00 = Label(root, text=f"Updates:", font=("Helvetica", 70))
lbl00.place(bordermode=OUTSIDE, anchor='nw', x=50, y=0, height=screen_height//8, width=screen_width//2.5)

lbl01 = Label(root, text=f"Water height is {y_water[-1]} cm", font=("Helvetica", 36))
lbl01.place(bordermode=OUTSIDE, anchor='nw', x=50, y=screen_height//8, height=screen_height//8, width=screen_width//2.5)

lbl02 = Label(root, text=f"Water needs to be changed at 5 cm", font=("Helvetica", 36))
lbl02.place(bordermode=OUTSIDE, anchor='nw', x=50, y=screen_height//4, height=screen_height//8-40, width=screen_width//2.5)

lbl03 = Label(root, text=f"Nutrient concentration is {y_nutrient[-1]}%", font=("Helvetica", 36))
lbl03.place(bordermode=OUTSIDE, anchor='nw', x=50, y=3*screen_height//8, height=screen_height//8-80, width=screen_width//2.5)

# Image
pathToImage = f"{os.getcwd()}/{data_folder}/flower.jpeg"
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
plot1.set_title("Water Usage Over Last 12 hours")
plot1.set_xlabel("Time")
plot1.set_ylabel("Height (cm)")

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
plot2.set_title("Nutrient Usage Over Last 12 hours")
plot2.set_xlabel("Time")
plot2.set_ylabel("Concentration (%)")

canvas2 = FigureCanvasTkAgg(fig2, master=root)  
canvas2.draw()
canvas2.get_tk_widget().place(bordermode=OUTSIDE, anchor='ne', x=screen_width-50, y=screen_height//2, height=screen_height//2.5, width=screen_width//2.5)

toolbar2 = NavigationToolbar2Tk(canvas2, root)
toolbar2.update()
toolbar2.place(bordermode=OUTSIDE, anchor='ne', x=screen_width-50, y=screen_height//2-40)

def update_screen():
    #system.run_system()
    x_water, y_water, x_nutrient, y_nutrient = update_data()
    root.after(1000, update_screen)

# Main Loop
root.after(1000, update_screen)
root.mainloop()

