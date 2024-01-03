# im: (N, M, 4) array-like of np.uint8 i.e. an array of RGBA pixels.
import numpy as np
from js import document, ImageData, HTMLCanvasElement, CanvasRenderingContext2D
from pyodide.ffi import create_proxy

from dataclasses import dataclass
from typing import List, cast


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


def clear_screen(image: Image, color: Color) -> None:
    for y in range(image.height):
        for x in range(image.width):
            image.pixels[y][x] = color


def draw_pixel(image: Image, x: int, y: int, color: Color) -> None:
    if 0 <= x < image.width and 0 <= y < image.height:
        image.pixels[y][x] = color


def create_image(width: int, height: int, background_color: Color) -> Image:
    return Image(
        width,
        height,
        [[background_color for _ in range(width)] for _ in range(height)],
    )


def draw_image(image: Image):
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

    # rendering the ImageData object onto a canvas element
    canvas_element = cast(HTMLCanvasElement, document.createElement("canvas"))
    canvas_element.id = "myCanv"  # TODO clean up names to disambiguate
    canvas_element.width = w
    canvas_element.height = h
    ctx = cast(CanvasRenderingContext2D, canvas_element.getContext("2d"))

    ctx.putImageData(img_data, 0, 0)
    ctx.drawImage(canvas_element, 0, 0)

    myCanv = document.getElementById("myCanv")
    if myCanv is not None:
        print("Removing old canvas")
        myCanv.remove()
    else:
        print("Existing canvas not found, attempting to create new one")

    pyCanv = document.getElementById("python-canvas")
    if pyCanv is not None:
        pyCanv.appendChild(canvas_element)
    else:
        print(
            """
            Could not find div to append canvs to. 
            There should be a div with 'python-canvas' id"
            """
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
