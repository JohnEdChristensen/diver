import diver as dv
import math as m
import time
WIDTH = 512
HEIGHT = 512

background_color = dv.Color(58, 81, 93) #3A515D



img = dv.create_image(WIDTH,HEIGHT,background_color)
for x in range(WIDTH):
    y = m.sin(40 * x/(HEIGHT))
    y = y*HEIGHT/4
    y = y+HEIGHT/2
    y = int(y)
    dv.draw_pixel(img,x,y,dv.Color(255,255,255))

dv.draw_image(img)
