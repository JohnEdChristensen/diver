from diver import CanvasManager, Color
import math as m
from dataclasses import dataclass
from typing import Tuple

WIDTH = 64
HEIGHT = WIDTH
print("hello from draw.py")


def update(self: CanvasManager, t):
    canvas = self.canvas
    ctx = self.ctx
    canvas.width = WIDTH
    canvas.height = HEIGHT

    img = self.create_image(WIDTH, HEIGHT, Color(0, 0, 0))

    particle_distance = WIDTH // 8
    p1 = particle(WIDTH // 2, HEIGHT // 2 + particle_distance // 2, 1)
    p2 = particle(WIDTH // 2, HEIGHT // 2 - particle_distance // 2, -1)

    for x in range(WIDTH):
        for y in range(HEIGHT):


            #calculate
            pixel_p1_distance = p1.distance(x, y)
            if pixel_p1_distance == 0:
                img.pixels[x][y] = (255, 155, 155, 255)
                continue

            pixel_p2_distance = p2.distance(x, y)
            if pixel_p2_distance == 0:
                img.pixels[x][y] = (155, 155, 255, 255)
                continue

            p1_field_strength = p1.charge / pixel_p1_distance**2
            p2_field_strength = p2.charge / pixel_p2_distance**2

            total_field = p1_field_strength + p2_field_strength
            #update
            #draw
            r,g,b,a = value_to_color(total_field, p2.charge, p1.charge)
            img.pixels[x][y] =(r,g,b,255)


    self.draw_image(img, 10)


canvasManager = CanvasManager(update)


@dataclass
class particle:
    x: int
    y: int
    charge: float

    def distance(self, xp, yp):
        # if particle is in center distance to each pixel < max(WIDTH,HEIGHT)/2
        dx = self.x - xp
        dy = self.y - yp
        return m.sqrt(dx**2 + dy**2)


def map_value(value, range1_min, range1_max, range2_min, range2_max):
    range1 = range1_max - range1_min
    range2 = range2_max - range2_min

    percent_of_range_1 = (value - range1_min) / range1

    return range2_min + (percent_of_range_1 * range2)


def value_to_color(value, min_value, max_value,exponential=.99)->Tuple[int,int,int,int]:
    val_range = max_value-min_value
    if abs(value) < val_range * .001:
    # if value==0:
        return (0, 0, 0, 255)  # Black

    # Assuming full intensity colors: blue for negative, red for positive
    blue = (0, 0, 255, 255)
    red = (255, 0, 0, 255)

    # Normalize value to [0, 1]
    if value < 0:
        value = -value
        normalized = (value - min_value) / (max_value - min_value)
        normalized = normalized ** (-exponential)
        # Interpolate between black and blue
        return tuple(int((1 - normalized) * c) for c in blue) # type: ignore
    else:
        normalized = (value - min_value) / (max_value - min_value)
        normalized = normalized ** (-exponential)
        # Interpolate between black and red
        return tuple(int((1 - normalized) * c) for c in red) # type: ignore


