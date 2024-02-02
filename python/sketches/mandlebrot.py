from diver import CanvasManager, Color
import math as m
import js

WIDTH = 100
HEIGHT = WIDTH
color_width = 5


background_color = Color(45, 53, 59)

c = "#d3c6aa"
c = Color(211, 198, 170)

count = js.document.getElementById("myCount")
if count is None:
    count = js.document.createElement("span")
    count.id = "myCount"
    count.textContent = "x*y is divisble by 0"
    js.document.getElementById("bar").appendChild(count)


nums = [3, 4, 5, 6]
comb = []
for i in nums:
    for j in reversed(nums):
        comb.append(i * j)
comb.sort()
comb = list(set(comb))


# this function will get called every frame
def update(canvas_manager: CanvasManager, time):
    # time is in milliseconds
    seconds = time / 1000
    start = 0
    end = len(comb)
    i = (int(seconds) % end) + start
    n = comb[i]
    count.textContent = f"x*y is divisble by {n}"
    w = n * 5 + 1
    base_size = comb[0] * 5 + 1
    scale = w / base_size
    img = canvas_manager.create_image(w, w, background_color)
    canvas_manager.ctx.scale(scale, scale)
    for y in range(w):
        for x in range(w):
            if y * x % n == 0:
                img.pixels[y][x] = (c.r, c.g, c.b, 255)

    canvas_manager.draw_image(img, 5)


# start the animation
CanvasManager(update)
