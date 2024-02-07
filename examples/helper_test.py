from proceso import Sketch as pSketch
from dataclasses import dataclass
from typing import TypedDict
from typing_extensions import Unpack
from enum import Enum, auto
from js import window
import math as m
import time

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

        self.world_offset_x = 0
        self.world_offset_y = 0
        self.world_zoom_scale = 1
        self.diver_draw_end_time = time.time()

    # proceso seems to not refresh self.window_width and height well
    def debug_screen(self, desc):
        self.push()
        # print(f"{desc:20},js       :{window.innerWidth:4},{window.innerHeight:4}")
        # print(f"{desc:20},p5 window:{self.window_width:4},{self.window_height:4}")
        # print(f"{desc:20},p5 canvas:{self.width:4},{self.height:4}")

        # print(self.screen_left, self.screen_middle_x, self.screen_right)
        # print(self.screen_bottom, self.screen_middle_y, self.screen_top)
        # Axis
        self.stroke("green")
        self.stroke_weight(5)
        self.line(
            self.screen_left + 1,
            self.screen_top,
            self.screen_left + 1,
            self.screen_bottom,
        )
        self.line(
            0,
            self.screen_top,
            0,
            self.screen_bottom,
        )
        self.line(
            self.screen_right - 1,
            self.screen_top,
            self.screen_right - 1,
            self.screen_bottom,
        )

        self.stroke("red")
        self.line(
            self.screen_left,
            self.screen_top - 1,
            self.screen_right,
            self.screen_top - 1,
        )
        self.line(
            self.screen_left,
            0,
            self.screen_right,
            0,
        )
        self.line(self.screen_left, self.screen_bottom, self.screen_right, self.screen_bottom)

        self.pop()

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

    def fill_screen(self):
        # print(self.world_zoom_scale)
        # init
        self.screen_bottom = -1 * window.innerHeight / 2
        self.screen_top = window.innerHeight / 2
        self.screen_left = -1 * window.innerWidth / 2
        self.screen_right = window.innerWidth / 2

        if self.width != window.innerWidth or self.height != window.innerHeight:
            print("resizing canvas")
            self.resize_canvas(window.innerWidth, window.innerHeight)

    def setup_screen(self):
        self.fill_screen()
        self.square_draw_area()

        if self.origin == Origin.CENTER:
            self.translate(self.width // 2, self.height // 2)
            self.scale(1, -1)

        # TODO make sure this works in both oriing modes
        self.translate(self.world_offset_x, self.world_offset_y)

        # TODO IMPORTANT Fix this... Grid lines should still work when moving
        self.screen_top -= self.world_offset_y
        self.screen_bottom -= self.world_offset_y
        self.screen_left -= self.world_offset_x
        self.screen_right -= self.world_offset_x
        # self.screen_middle_y = (self.screen_top + self.screen_bottom) // 2
        # self.screen_middle_x = (self.screen_left + self.screen_right) // 2

        s = 1 / self.world_zoom_scale
        self.screen_bottom *= s
        self.screen_top *= s
        self.screen_left *= s
        self.screen_right *= s

    def apply_zoom(self, s):
        self.world_zoom_scale = self.world_zoom_scale * s
        self.world_zoom_scale = max(min(self.world_zoom_scale, 2.0), 0.1)
        # print(self.world_zoom_scale)
        # world_mouse_x = self.mouse_x - self.width // 2
        # world_mouse_y = -1 * (self.mouse_y - self.height // 2)
        # self.world_offset_x = world_mouse_x * (1 - s) + self.world_offset_x * s
        # self.world_offset_y = world_mouse_y * (1 - s) + self.world_offset_y * s
        # print(self.world_offset_x, self.world_offset_y)
        # print(world_mouse_x, world_mouse_y)

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
        print(f"time between loop: {self.diver_draw_end_time - time.time()}")
        self.diver_start_draw_time = time.time()
        speed = 10
        if self.key_is_down(self.RIGHT_ARROW):  # type: ignore
            self.world_offset_x -= speed
        if self.key_is_down(self.LEFT_ARROW):  # type: ignore
            self.world_offset_x += speed
        if self.key_is_down(self.UP_ARROW):  # type: ignore
            self.world_offset_y -= speed
        if self.key_is_down(self.DOWN_ARROW):  # type: ignore
            self.world_offset_y += speed

        # setup world units
        self.setup_screen()
        self.scale(self.world_zoom_scale)

        self.clear()

        print(f"diver setup time: {self.diver_start_draw_time - time.time()}")
        # self.debug_screen("draw")
        # finally call user's draw
        self.user_draw_start_time = time.time()
        self.user_draw()
        self.diver_draw_end_time = time.time()
        print(f"user draw  time: {self.user_draw_start_time - self.diver_draw_end_time}")

    def mouse_wheel(self, event):
        scale = 1.05 if event.deltaY > 0 else 0.95

        self.apply_zoom(scale)

    def start(self, user_setup, user_draw):
        self.user_setup = user_setup
        self.user_draw = user_draw

        self.run_sketch(setup=self.diver_setup, draw=self.diver_draw, mouse_wheel=self.mouse_wheel)


p5 = Sketch()


def setup():
    ...
    p5.create_canvas(300, 300, "WEBGL")
    # p5.save_gif("mySketch", 5)


def draw():
    p5.push()

    # grid lines
    num_ticks = 20

    tick_size = p5.figure_width // num_ticks
    major_tick_freq = 5

    # start = tick_size * round(p5.screen_left / tick_size)
    # stop = tick_size * round(p5.screen_right / tick_size)
    # for x1 in range(start, stop, tick_size):
    #     if x1 % (major_tick_freq * tick_size) == 0:
    #         p5.stroke("lightgrey")
    #     else:
    #         p5.stroke("grey")
    #     p5.line(x1, p5.screen_top, x1, p5.screen_bottom)
    #
    # start = tick_size * round(p5.screen_bottom / tick_size)
    # stop = tick_size * round(p5.screen_top / tick_size)
    # for x1 in range(start, stop, tick_size):
    #     if x1 % (major_tick_freq * tick_size) == 0:
    #         p5.stroke("lightgrey")
    #     else:
    #         p5.stroke("grey")
    #     p5.line(p5.screen_left, x1, p5.screen_right, x1)
    #
    # # Axis
    # p5.stroke("green")
    # p5.line(0, p5.screen_top, 0, p5.screen_bottom)
    # p5.stroke("red")
    # p5.line(p5.screen_left, 0, p5.screen_right, 0)

    # Big  circle
    # p5.stroke_weight(2)
    # t = p5.millis() / 2000
    # r = sin(t) * p5.figure_width // 2
    # p5.fill("blue")
    # p5.circle(0, 0, 2 * r)
    # p5.fill("white")
    #
    # # moving labels
    # p5.text_size(tick_size * 2)
    # p5.text_descent
    #
    # p5.stroke("black")
    # p5.fill("red")
    # p5.text(f"{(r / tick_size):.1f}", r, 0)
    # p5.no_stroke()
    # p5.circle(r, 0, tick_size / 4)
    #
    # p5.stroke("black")
    # p5.fill("green")
    # p5.text(f"{(r / tick_size):.1f}", 0, r)
    # p5.no_stroke()
    # p5.circle(0, r, tick_size / 4)

    p5.stroke("white")
    p5.color_mode(p5.HSL)
    p5.stroke("0,100,100")
    p5.stroke_weight(4)
    r = 200
    x1 = y1 = None
    x2 = y2 = None
    for i in range(int(p5.screen_bottom), int(p5.screen_top), 2):
        t = i / 100 * 2 * m.pi + p5.millis() / 500
        xp1 = m.sin(t) * r
        yp1 = i * 2
        xp2 = m.cos(t * 0.8 + m.pi / 2) * r
        yp2 = i * 2.01
        if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
            p5.stroke(y1 % 360, 50, 50)
            p5.line(x1, y1, xp1, yp1)
            p5.stroke(int((y2 + i) % 360), 50, 50)
            p5.line(x2, y2, xp2, yp2)
        x1 = xp1
        y1 = yp1
        x2 = xp2
        y2 = yp2

    p5.pop()


p5.start(setup, draw)
