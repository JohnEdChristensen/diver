# Musical Bubbles
# based on code from Keith Peters. Multiple-object collision.
# Adapted from https://p5js.org/examples/motion-bouncy-bubbles.html
# Port to pyscript by Ben Alkov, 2022-07
# Oscillator sound added by Andrew Hannum, 2022-07

import math

from diver import CanvasManager
import math as m

# Not strictly necessary, but seeing naked e.g. `document`, `window`, etc. really bothers me
import js
import random

# import p5
from proceso import Sketch


NUM_BALLS = 10
SPRING = 0.9
GRAVITY = 0.03
FRICTION = -0.9
BALLS = []
HEIGHT = 400
WIDTH = 720


class Ball:
    def __init__(self, x, y, dia):
        self.x = x
        self.y = y
        self.diameter = dia
        self.vx = 0
        self.vy = 0
        self.osc = js.p5.Oscillator.new()
        self.osc.freq(440)
        self.env = js.p5.Envelope.new(0.1, 0.1, 0.1, 0.1)
        self.osc.amp(self.env)
        self.osc.start()

    def collide(self):
        for other_ball in [b for b in BALLS if b is not self]:
            dx = other_ball.x - self.x
            dy = other_ball.y - self.y
            distance = math.sqrt(dx * dx + dy * dy)
            min_dist = other_ball.diameter / 2 + self.diameter / 2
            if distance < min_dist:
                angle = math.atan2(dy, dx)
                targetX = self.x + math.cos(angle) * min_dist
                targetY = self.y + math.sin(angle) * min_dist
                ax = (targetX - other_ball.x) * SPRING
                ay = (targetY - other_ball.y) * SPRING
                self.vx -= ax
                self.vy -= ay
                other_ball.vx += ax
                other_ball.vy += ay
                # self.env.play()

    def move(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        if self.x + self.diameter / 2 > WIDTH:
            self.x = WIDTH - self.diameter / 2
            self.vx *= FRICTION
        elif self.x - self.diameter / 2 < 0:
            self.x = self.diameter / 2
            self.vx *= FRICTION

        if self.y + self.diameter / 2 > HEIGHT:
            self.y = HEIGHT - self.diameter / 2
            self.vy *= FRICTION
        elif self.y - self.diameter / 2 < 0:
            self.y = self.diameter / 2
            self.vy *= FRICTION

    def display(self):
        p5js.ellipse(self.x, self.y, self.diameter, self.diameter)


# These are named per convention: p5.js doesn't know anything about them


def draw():
    p5js.background(45, 53, 59)
    p5js.stroke(255)
    p5js.no_fill()
    p5js.rect(1, 1, WIDTH - 1, HEIGHT - 1)
    for ball in BALLS:
        ball.collide()
        ball.move()
        ball.display()


def setup():
    global BALLS
    p5js.create_canvas(WIDTH, HEIGHT)
    BALLS = [
        Ball(p5js.random(WIDTH), p5js.random(HEIGHT), p5js.random(30, 70))
        for _ in range(NUM_BALLS)
    ]
    p5js.no_stroke()
    p5js.fill(255, 204)
    p5js.background(45, 53, 59)


p5js = Sketch()
p5js.run_sketch(setup=setup, draw=draw)
