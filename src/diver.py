from dataclasses import dataclass
from typing import Callable, List, cast,Any

import numpy as np
from js import (
    CanvasRenderingContext2D,
    HTMLCanvasElement,
    ImageData,
    document,
    window,
)
from pyodide.ffi import create_proxy


@dataclass
class Color:
    r: int
    g: int
    b: int


@dataclass
class Image:
    width: int
    height: int
    pixels: List[List[Color]]


class CanvasManager:
    def __init__(self, animate_func):
        print("hello from CanvasManager, ('diver.py')")
        self.animate_func = animate_func
        self.animate_loop_proxy = create_proxy(self.animate_loop)
        self.canvas = cast(HTMLCanvasElement, document.getElementById("myCanv"))
        if self.canvas is None:
            print("Existing canvas not found, attempting to create new one")
            self.canvas = cast(HTMLCanvasElement, document.createElement("canvas"))
            self.canvas.id = "myCanv"  # TODO clean up names to disambiguate
        self.ctx = cast(CanvasRenderingContext2D, self.canvas.getContext("2d"))
        self.last_frame_id = 0
        self.start_time = 0
        self.start()

    # animation info

    def start(self):
        window.cancelAnimationFrame(self.last_frame_id)
        # a proxy is necessary to pass a python function to js
        # this starts the animation (and keeps track of the current frame)
        self.last_frame_id = window.requestAnimationFrame(
            self.animate_loop_proxy
        )

    def animate_loop(self, frame_time_mili):
        self.animate_func(self,frame_time_mili)
        self.last_frame_id = window.requestAnimationFrame(
            self.animate_loop_proxy
        )

    def clear_screen(self, image: Image, color: Color) -> None:
        for y in range(image.height):
            for x in range(image.width):
                image.pixels[y][x] = color

    def draw_pixel(self, image: Image, x: int, y: int, color: Color) -> None:
        if 0 <= x < image.width and 0 <= y < image.height:
            image.pixels[y][x] = color

    def create_image(
        self, width: int, height: int, background_color: Color
    ) -> Image:
        return Image(
            width,
            height,
            # [[Color(0,0,0) for _ in range(width)] for _ in range(height)],
            [[background_color for _ in range(width)] for _ in range(height)],
        )

    def draw_image(self, image: Image):
        canvas = self.canvas
        height = image.height
        width = image.width
        numpy_image = np.zeros((height, width, 4), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                c = image.pixels[y][x]
                # Assuming the alpha channel is always 255 (fully opaque)
                numpy_image[y, x] = [c.r, c.g, c.b, 255]

        h, w, d = numpy_image.shape
        numpy_image = np.ravel(
            np.uint8(np.reshape(numpy_image, (h * w * d, -1)))
        ).tobytes()

        pixels_proxy = create_proxy(numpy_image)
        pixels_buf = pixels_proxy.getBuffer("u8clamped")
        img_data = ImageData.new(pixels_buf.data, w, h)

        self.ctx.putImageData(img_data, 0, 0)
        self.ctx.drawImage(canvas, 0, 0)

        pyCanv = document.getElementById("python-canvas-container")
        if pyCanv is not None:
            pyCanv.appendChild(canvas)
        else:
            print(
                "Could not find div to append canvs to.",
                "There should be a div with 'python-canvas-container' id",
            )

        pixels_proxy.destroy()
        pixels_buf.release()
        return "Created Image", w, h


# Example usage
# background_color = Color(1, 128, 128)
# img = create_image(100, 100, background_color)
# Clear the screen with the background color
# clear_screen(img, background_color)
# draw_pixel(img, 10, 10, Color(255, 0, 0))  # Draw a red pixel at (10, 10)
#
#
# draw_image(img)
