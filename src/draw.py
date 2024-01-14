from diver import CanvasManager, Color
import math as m
from js import window
from pyodide.ffi import create_proxy

WIDTH =128 
HEIGHT = WIDTH 
print("hello from draw.py")
background_color = Color(58, 81, 93)  # 3A515D
last_time = 0

def update(self,t):
    img = self.create_image(WIDTH, HEIGHT, background_color)
    print(t)
    for x in range(WIDTH):
        y = m.sin(40 * x / (HEIGHT) - t/1000 * 4)
        y = y * HEIGHT / 4
        y = y + HEIGHT / 2
        y = int(y)
        self.draw_pixel(img, x, y, Color(255, 255, 255))

    self.draw_image(img)

canvasManager = CanvasManager(update)
