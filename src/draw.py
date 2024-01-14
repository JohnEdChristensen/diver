from diver import CanvasManager, Color
import math as m
from js import window
from pyodide.ffi import create_proxy

WIDTH =128 
HEIGHT = WIDTH 
print("hello from draw.py")
background_color = Color(43, 51, 57) #2b3339


red = Color(255, 0, 0) #ff0000
orange = Color(255, 165, 0) #ffa500
yellow = Color(255, 255, 0) #ffff00
green = Color(0, 128, 0) #008000
blue = Color(0, 0, 255) #0000ff
indigo = Color(75, 0, 130) #4b0082
violet = Color(238, 130, 238) #ee82ee

colors = [red,orange,yellow,green,blue,indigo,violet]
colors.reverse()

def update(self: CanvasManager,t):
    img = self.create_image(WIDTH, HEIGHT, background_color)
    #print(t)
    for i,color in enumerate(colors):
        for x in range(WIDTH):
            y = m.sin(20 * x / (HEIGHT) - t/1000 * 4)
            y_scale = m.sin(x/WIDTH * m.pi)
            y= y*y_scale
            y = y * HEIGHT / 5
            y = y + HEIGHT / 2
            y = int(y)
            color_width = 6
            y = y-(i*(color_width-1))
            for j in range(color_width-1):
                self.draw_pixel(img, x, y-j,color)

    self.draw_image(img,4)

canvasManager = CanvasManager(update)
