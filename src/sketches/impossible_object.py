from diver import CanvasManager
import math as m

WIDTH = 600
HEIGHT = WIDTH
print("hello from draw.py")


c1 = "#71847B"
c2 = "#859289"
c3 = "#9DA9A0"
cf = "#d3c6aa"


def update(self: CanvasManager, t):
    canvas = self.canvas
    ctx = self.ctx
    canvas.width = WIDTH
    canvas.height = HEIGHT
    w, h = WIDTH, HEIGHT
    rotate_angle = t / 1000

    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    #put orign at bottom right
    ctx.translate(0, h)
    ctx.scale(20,-20) 
    ## add some margin
    ctx.translate(10,10)

    ctx.translate(6,5)
    ctx.rotate(t/1000)
    xLength = 2
    yLength = m.sqrt(3)
    ycorrection = yLength/xLength
    scalex = 1 + .1 * m.sin(t/1000)
    scaley = 1 + .3 * m.sin(t/500)
    ctx.scale(1*scalex,ycorrection* scaley)
    ctx.translate(-6,-5)
    # start sketching
    # side 1 
    ctx.lineWidth=.1
    ctx.strokeStyle=cf
    ctx.fillStyle = c3
    ctx.beginPath()
    ctx.moveTo(0,2)
    ctx.lineTo(5,12)
    ctx.lineTo(9,4)
    ctx.lineTo(7,4)
    ctx.lineTo(5,8)
    ctx.lineTo(1,0)
    ctx.closePath()
    ctx.fill()
    ctx.stroke()

    # side 2 
    ctx.fillStyle = c1
    ctx.beginPath()
    ctx.moveTo(4,2)
    ctx.lineTo(5,4)
    ctx.lineTo(9,4)
    ctx.lineTo(5,12)
    ctx.lineTo(7,12)
    ctx.lineTo(12,2)
    ctx.closePath()
    ctx.fill()
    ctx.stroke()

    # side 3 
    ctx.fillStyle = c2
    ctx.beginPath()
    ctx.moveTo(1,0)
    ctx.lineTo(11,0)
    ctx.lineTo(12,2)
    ctx.lineTo(4,2)
    ctx.lineTo(6,6)
    ctx.lineTo(5,8)
    ctx.closePath()
    ctx.fill()
    ctx.stroke()



        
    # ctx.fillStyle = c2
    # ctx.fillRect(0,0,10,10)
    # ctx.fillStyle = c3
    # ctx.fillRect(0,0,10,10)
    
    ctx.stroke()


canvasManager = CanvasManager(update)
