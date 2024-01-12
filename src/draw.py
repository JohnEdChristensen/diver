import diver as dv
import math as m
from js import window
from pyodide.ffi import create_proxy

WIDTH =128 
HEIGHT = WIDTH 

window.cancelAnimationFrame(dv.lastFrameId)
background_color = dv.Color(58, 81, 93)  # 3A515D
last_time = 0


def update(t):
    global last_time
    dt = t - last_time
    print(dt)
    last_time = t
    img = dv.create_image(WIDTH, HEIGHT, background_color)
    for x in range(WIDTH):
        y = m.sin(40 * x / (HEIGHT) - t/1000 * 4)
        y = y * HEIGHT / 4
        y = y + HEIGHT / 2
        y = int(y)
        dv.draw_pixel(img, x, y, dv.Color(255, 255, 255))

    dv.draw_image(img)
    proxy = create_proxy(update)
    dv.lastFrameId = window.requestAnimationFrame(proxy)


proxy = create_proxy(update)
window.requestAnimationFrame(proxy)
