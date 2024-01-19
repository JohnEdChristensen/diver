from diver import CanvasManager, Color
import math as m

WIDTH = 128
HEIGHT = WIDTH
color_width = 5


background_color = Color(45, 53, 59)
red = Color(255, 0, 0)
orange = Color(255, 165, 0)
yellow = Color(255, 255, 0)
green = Color(0, 128, 0)
blue = Color(0, 0, 255)
indigo = Color(75, 0, 130)
violet = Color(238, 130, 238)

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
        
        #starting at violet, draw bands of color
        for i, color in enumerate(colors):
            for j in range(color_width):
                img.draw_pixel(x, y, color)
                y = y - 1  # move up 1 to draw the next pixel

    canvas_manager.draw_image(img, 4)


# start the animation
CanvasManager(update)
