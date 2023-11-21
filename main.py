# im: (N, M, 4) array-like of np.uint8 i.e. an array of RGBA pixels.
import numpy as np
from js import document, ImageData
from pyodide.ffi import create_proxy
def create_debug_image(width, height):
    # Create an empty image with RGBA channels
    image = np.zeros((height, width, 4), dtype=np.uint8)

    # Red, Green, and Blue sections
    red_section = height // 3
    green_section = 2 * height // 3

    image[:red_section, :, 0] = 255  # Red channel
    image[red_section:green_section, :, 1] = 255  # Green channel
    image[green_section:, :, 2] = 255  # Blue channel

    # Gradient (horizontal)
    for x in range(width):
        gradient_intensity = x / width
        image[:, x, :3] = image[:, x, :3] * gradient_intensity

    # Transparency gradient (vertical)
    for y in range(height):
        alpha_intensity = y / height
        image[y, :, 3] = int(255 * alpha_intensity)

    # Adding a grid for pixel position
    grid_color = 255  # White grid
    grid_spacing = 64
    for x in range(0, width, grid_spacing):
        image[:, x] = grid_color
    for y in range(0, height, grid_spacing):
        image[y, :] = grid_color

    return image

# Create the debug image with specified dimensions
im = create_debug_image(512, 512)
# converting numpy array to an ImageData object
# through Uint8ClampedArray representation
h, w, d = im.shape
im = np.ravel(np.uint8(np.reshape(im, (h * w * d, -1)))).tobytes()




pixels_proxy = create_proxy(im)
pixels_buf = pixels_proxy.getBuffer("u8clamped")
img_data = ImageData.new(pixels_buf.data, w, h)

# rendering the ImageData object onto a canvas element
canvas_element = document.createElement("canvas")
canvas_element.id = "myCanv" #TODO clean up names to disambiguate
canvas_element.width = w
canvas_element.height = h
ctx = canvas_element.getContext("2d")
ctx.putImageData(img_data, 0, 0)
ctx.drawImage(canvas_element,0,0)


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
    print("Could not find div to append canvs to. There should be a div with 'python-canvas' id")
# clean-up
pixels_proxy.destroy()
pixels_buf.release()

"Created Image",w,h
