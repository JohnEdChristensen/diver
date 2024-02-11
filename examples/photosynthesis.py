# from https://proceso.cc/examples/creative_coding/
from diver import Sketch
import numpy as np
from dataclasses import dataclass

p5 = Sketch()


p5.setup_screen()
num_bubbles = 50
growth_scale = 10

# leaf
leaf_height = p5.figure_width / 5
leaf_length = p5.figure_width
leaf_vertical_pos = p5.figure_bottom + leaf_height
bubble_spacing = leaf_length / num_bubbles


# bubbles
@dataclass
class Bubble:
    x: float
    y: float
    growth_rate: float
    diameter = 0
    is_rising = False
    speed = 0.2
    # max_size = bubble_spacing*2 # bubbles will never rise before merging
    max_size = bubble_spacing * 1.5
    eccentricity = 1.0

    def update(self):
        if self.is_rising is False:
            self.diameter += self.growth_rate
            self.check_rising()
        else:
            # Approximation of boyant force...
            # could add a damping term to account for
            # greater resistance for larger bubbles
            self.y += self.speed

    def check_rising(self):
        if self.diameter > self.max_size:
            # start a new bubble where this one left off
            rising_bubble = Bubble(self.x, self.y, 0)
            rising_bubble.is_rising = True
            rising_bubble.diameter = self.diameter
            rising_bubble.speed *= np.sqrt(self.diameter)
            bubbles.append(rising_bubble)
            self.diameter = 0

    def draw(self):
        p5.ellipse(self.x, self.y, self.diameter, self.diameter * self.eccentricity)


xs = np.linspace(-leaf_length / 2, leaf_length / 2, num_bubbles)

p5.background("steelblue")


def ellipse_y(x, width, height) -> tuple[float, float]:
    """give positive +-y as a function of x for an ellipse"""
    y = np.sqrt(1 - x**2 / (width / 2) ** 2) * (height / 2)
    return (-y, y)


bubbles = [
    Bubble(
        x + p5.random(-bubble_spacing / 4, bubble_spacing / 4),
        # leaf_vertical_pos + p5.random(*ellipse_y(x, leaf_length, leaf_height)),
        leaf_vertical_pos + ellipse_y(x, leaf_length, leaf_height)[1],
        growth_scale * p5.random(0.00001, 0.01),
    )
    for x in xs
]


def draw():
    global bubbles
    p5.background("steelblue")
    # p5.stroke("black")
    # p5.rect(p5.figure_left, p5.figure_bottom, p5.figure_width, p5.figure_height)

    # leaf
    p5.stroke("darkgreen")
    p5.fill("seagreen")
    p5.ellipse(0, leaf_vertical_pos, leaf_length, leaf_height)

    for bubble in bubbles:
        bubble.update()

    def bubbles_overlap(bubble1: Bubble, bubble2: Bubble) -> bool:
        distance = np.sqrt((bubble1.x - bubble2.x) ** 2 + (bubble1.y - bubble2.y) ** 2)
        combined_width = bubble1.diameter / 2 + bubble2.diameter / 2
        if distance < combined_width - 1:
            return True
        else:
            return False

    pairs = zip(bubbles, bubbles[1:])

    overlapping_pairs = filter(lambda pair: bubbles_overlap(pair[0], pair[1]), pairs)

    for pair in overlapping_pairs:
        left_area = np.pi * (pair[0].diameter / 2) ** 2
        right_area = np.pi * (pair[1].diameter / 2) ** 2

        right_final_area = left_area + right_area
        right_final_radius = np.sqrt(right_final_area / np.pi)
        pair[1].diameter = right_final_radius * 2
        pair[1].eccentricity *= 0.99
        pair[1].eccentricity = max(0.9, pair[1].eccentricity)
        pair[1].check_rising()
        # if not pair[1].is_rising:
        #     pair[1].x -= bubble_spacing / 2

        # for now, just reset the left bubble
        pair[0].diameter = 0
        # pair[0].x -= bubble_spacing / 2

    # remove bubbles after they get too high
    bubbles = list(filter(lambda bubble: bubble.y < p5.figure_top, bubbles))

    p5.no_fill()
    p5.stroke("white")
    for bubble in bubbles:
        bubble.draw()

    # xs = np.linspace(p5.figure_left, p5.figure_right, num_bubbles)
    # for x in xs:
    #     ny, y = ellipse_y(x, leaf_length, leaf_height)
    #     print(ny, y)
    #     p5.stroke("red")
    #     p5.circle(x, leaf_vertical_pos + y, 2)
    #     p5.stroke("blue")
    #     p5.circle(x, leaf_vertical_pos + ny, 2)


def setup():
    ...


p5.start(setup, draw)
