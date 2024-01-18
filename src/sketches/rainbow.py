from diver import CanvasManager, Color
import math as m

WIDTH = 128
HEIGHT = WIDTH
color_width = 5


background_color = Color(43, 51, 57)  # 2b3339
red = Color(255, 0, 0)  # ff0000
orange = Color(255, 165, 0)  # ffa500
yellow = Color(255, 255, 0)  # ffff00
green = Color(0, 128, 0)  # 008000
blue = Color(0, 0, 255)  # 0000ff
indigo = Color(75, 0, 130)  # 4b0082
violet = Color(238, 130, 238)  # ee82ee

colors = [red, orange, yellow, green, blue, indigo, violet]
colors.reverse()


# this function will get called every frame
def update(canvas_manager: CanvasManager, time):
    img = canvas_manager.create_image(WIDTH, HEIGHT, background_color)
    # time is in milliseconds
    seconds = time / 1000

    for x in range(WIDTH):
        first_wave = m.sin(20 * x / (HEIGHT) - seconds * 4)
        y = first_wave
        second_wave = m.sin(x / WIDTH * m.pi)
        y = y * second_wave
        y = y * HEIGHT / 5  # scale it some more
        y = y + HEIGHT / 2  # shift it to be centered
        y = int(y)

        for i, color in enumerate(colors):
            for j in range(color_width):
                canvas_manager.draw_pixel(img, x, y-(i*color_width +j), color)

    canvas_manager.draw_image(img, 4)


# start the animation
CanvasManager(update)
