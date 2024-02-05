from math import sin
from proceso import Sketch as pSketch
from dataclasses import dataclass
from typing import TypedDict
from typing_extensions import Unpack
from enum import Enum, auto
from js import window

SCREEN_WIDTH = SCREEN_HEIGHT = WIDTH = HEIGHT = 0


class Origin(Enum):
    CENTER = auto()
    TOP_LEFT = auto()


class SketchConfig(TypedDict, total=False):
    margin: int
    auto_fill_screen: bool
    origin: Origin


@dataclass
class Sketch(pSketch):
    def __init__(self, **options: Unpack[SketchConfig]):
        super().__init__()
        self.margin = options.get("margin", 50)
        self.origin = options.get("origin", Origin.CENTER)
        self.auto_fill_screen = options.get("auto_fill_screen")

        self._update_system_variables()

    # proceso seems to not refresh self.window_width and height well
    def debug_screen(self, desc):
        print(f"{desc:20},js       :{window.innerWidth:4},{window.innerHeight:4}")
        print(f"{desc:20},p5 window:{self.window_width:4},{self.window_height:4}")
        print(f"{desc:20},p5 canvas:{self.width:4},{self.height:4}")

    def square_draw_area(self):
        """set the width and height as large as possible while still square"""
        figure_width = window.innerWidth - 2 * self.margin
        figure_height = window.innerHeight - 2 * self.margin

        # Make a square drawing area, based on the smaller dimension
        self.figure_width = min(figure_width, figure_height)
        self.figure_height = figure_width
        self.figure_bottom = -self.figure_height // 2
        self.figure_top = self.figure_height // 2
        self.figure_left = -self.figure_width // 2
        self.figure_right = self.figure_width // 2

        self.screen_bottom = -window.innerHeight // 2
        self.screen_top = window.innerHeight // 2
        self.screen_left = -window.innerWidth // 2
        self.screen_right = window.innerWidth // 2

    def fill_screen(self):
        if self.width == window.innerWidth and self.height == window.innerHeight:
            # already filling the screen
            return
        self.resize_canvas(window.innerWidth, window.innerHeight)

    def setup_screen(self):
        self.fill_screen()
        self.square_draw_area()

        if self.origin == Origin.CENTER:
            self.translate(self.width // 2, self.height // 2)
            self.scale(1, -1)

    #
    def text(
        self,
        txt: str,
        x: float,
        y: float,
        x2: float | None = None,
        y2: float | None = None,
    ) -> None:
        """Override p5js text to handle flipping y axis for text"""
        self.push()
        if self.origin == Origin.CENTER:
            self.scale(1, -1)
            y = -y
            if y2 is not None:
                y2 = -y2
        pSketch.text(self, txt, x, y, x2, y2)
        self.pop()
        return

    def diver_setup(self):
        self.setup_screen()
        self.user_setup()

    def diver_draw(self):
        self.setup_screen()
        self.user_draw()

    def start(self, user_setup, user_draw):
        self.user_setup = user_setup
        self.user_draw = user_draw

        self.run_sketch(setup=self.diver_setup, draw=self.diver_draw)


p5 = Sketch()


def setup():
    ...
    # p5.create_canvas(300, 300)


def draw():
    p5.clear()
    p5.push()

    # grid lines
    num_ticks = 20

    tick_size = p5.figure_width // num_ticks
    major_tick_freq = 5

    # start at 0, to make sure the grid goes through zero
    for i, y in enumerate(range(0, p5.screen_right, tick_size)):
        if i % major_tick_freq == 0:
            p5.stroke("lightgrey")
        else:
            p5.stroke("grey")
        p5.line(y, p5.screen_top, y, p5.screen_bottom)
        p5.line(-y, p5.screen_top, -y, p5.screen_bottom)

    for i, y in enumerate(range(0, p5.screen_top, tick_size)):
        if i % major_tick_freq == 0:
            p5.stroke("lightgrey")
        else:
            p5.stroke("grey")
        p5.line(p5.screen_left, y, p5.screen_right, y)
        p5.line(p5.screen_left, -y, p5.screen_right, -y)

    # Axis
    p5.stroke("white")
    p5.line(0, p5.screen_top, 0, p5.screen_bottom)
    p5.line(p5.screen_left, 0, p5.screen_right, 0)

    # Big  circle
    p5.stroke_weight(2)
    t = p5.millis() / 2000
    r = sin(t) * p5.figure_width // 2
    p5.fill("blue")
    p5.circle(0, 0, 2 * r)
    p5.fill("white")

    # moving labels

    p5.text_size(tick_size * 2)
    p5.text_descent

    p5.stroke("black")
    p5.fill("red")
    p5.text(f"{(r / tick_size):.1f}", r, 0)
    p5.no_stroke()
    p5.circle(r, 0, tick_size / 4)

    p5.stroke("black")
    p5.fill("green")
    p5.text(f"{(r / tick_size):.1f}", 0, r)
    p5.no_stroke()
    p5.circle(0, r, tick_size / 4)

    p5.pop()


p5.start(setup, draw)
