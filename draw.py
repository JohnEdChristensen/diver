from diver import Color, create_image,draw_pixel,draw_image
import math as m
WIDTH = 128
HEIGHT = 128

background_color = Color(58, 81, 93) #3A515D

img = create_image(WIDTH,HEIGHT,background_color)

for i in range(10):
# draw sin

    for x in range(WIDTH):
        y = m.sin(20 * (x+ i)/(WIDTH))
        y = y*WIDTH/4
        y = y+WIDTH/2
        y = int(y)
        draw_pixel(img,x,y,Color(255,255,255))


    draw_image(img)
    print("hello")
