# from https://proceso.cc/examples/creative_coding/
from proceso import Sketch


p5 = Sketch()
p5.describe("A purple circle moving in a figure eight on a light blue background.")


def setup():
    p5.create_canvas(400, 400)
    p5.background("dodgerblue")


def draw():
    p5.translate(p5.width * 0.5, p5.height * 0.5)
    x = 80 * p5.cos(0.1 * p5.frame_count)
    y = 40 * p5.sin(0.2 * p5.frame_count)
    p5.stroke("white")
    p5.fill("orchid")
    p5.circle(x, y, 20)
    if p5.is_mouse_pressed:
        p5.background("dodgerblue")


p5.run_sketch(setup=setup, draw=draw)
