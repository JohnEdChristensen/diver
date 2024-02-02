from proceso import Sketch
from numpy import interp
from js import window

p5 = Sketch()

WIDTH, HEIGHT = p5.width, p5.height


def setup():
    p5.resize_canvas(window.innerWidth, window.innerHeight)
    p5.background(0)


def draw():
    p5.second()
    s = p5.millis()
    o1 = (p5.sin(s / 1000),)
    color = int(interp(o1, [-1, 1], [0, 255]))
    p5.background(color)


p5.run_sketch(setup=setup, draw=draw)
