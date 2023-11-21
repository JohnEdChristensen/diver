import js

div = js.document.createElement("div")
div.innerHTML = """
<h1 style='color: red'>Hello From python! and Vim</h1>
"""

canvas = js.document.createElement("canvas")

if js.document.body is not None:
    js.document.body.append(div)
    js.document.body.append(canvas)
