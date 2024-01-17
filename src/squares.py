from diver import CanvasManager
import math as m

WIDTH =1024 
HEIGHT = WIDTH 
print("hello from draw.py")



def update(self: CanvasManager,t):
    canvas = self.canvas
    ctx = self.ctx
    canvas.width=WIDTH
    canvas.height=HEIGHT
    w,h=WIDTH,HEIGHT
    
    def draw_square(size):
        ctx.strokeRect(-size,-size,size*2,size*2)
         
    
    ctx.clearRect(0,0,canvas.width,canvas.height)
     
    ctx.save()
    ctx.strokeStyle = "#d3c6aa"
    ctx.translate(w * 0.5, h * 0.5)
    rotate_angle = t/1000
    ctx.rotate(rotate_angle)
    ctx.lineWidth = 2
    for i in range(1,20):
        ctx.rotate((m.pi/32 * m.sin(rotate_angle)))
        draw_square(15* (i+m.sin(.3*i*rotate_angle + m.pi/4)))
    ctx.restore()


canvasManager = CanvasManager(update)
