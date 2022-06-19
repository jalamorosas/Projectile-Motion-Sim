#GlowScript 3.0 VPython
from vpython import *
scene = canvas(title='Soccer Ball Physics',
     width=1000, height=450, texture = "https://i.imgur.com/IHAgVTv.jpg")
scene.forward = vector(-1,-0.3,-1)

base = box(pos = vector(0, -.02, 0), size = vector(5, .04, .5), color = color.white, texture = "https://i.imgur.com/VTdRekj.jpg")

running = False
global running

gp=gcurve(color=color.blue, label='Position (m)')
gv=gcurve(color=color.orange, label='velocity (m/s)')
ga=gcurve(color=color.yellow, label='acceleration (m/s^2)')

def textUpdate(textName, vectorName):
    return textName.pos = vec(vectorName.pos.x + (vectorName.axis.x) , vectorName.pos.y + (vectorName.axis.y), vectorName.pos.z)
    

def launch(ballHeight, magnitude, angle, rho):
    running = True
    
    for obj in scene.objects:
        if obj == base:
            obj.visible = True
        else:
            obj.visible = False
            del obj
        for light in scene.lights:
            if isinstance(light, local_light):
                light.visible = False
                del light
    initVectors()
    
    angle = angle * pi/180
    
    ball = sphere(pos = vec(-1.5, ballHeight + 0.05 ,0), radius = 0.05, make_trail = True, emissive = True, color = color.white, texture = "https://i.imgur.com/8UQs5v1.jpg")
    light = local_light(pos=ball.pos, color=ball.color, visible = True)
    ball.m = 0.01
    ball.p = vec(magnitude * cos(angle), magnitude * sin(angle), 0) * ball.m
    
    g = vec(0, -9.8, 0)
    t = 0
    dt = 0.01
    
    #rho = 1.2
    C = .47
    A = pi*ball.radius**2
    
    dist = 0.05
    
    
    gVector = arrow(radius = 0.02, pos = ball.pos, axis = norm(g) * 0.25, color = color.red)
    pVector = arrow(radius = 0.02, pos = ball.pos, axis = norm(ball.p) * 0.25, color = color.blue)
    airResisVec = arrow(radius = 0.02, pos = ball.pos, color = color.yellow) 

    
    gLabel = text(text = 'gravity', pos=ball.pos, color=color.red, billboard=True, emissive=True, height = 0.075)
    arLabel = text(text = 'air resistance', pos=ball.pos, color=color.yellow, billboard=True, emissive=True, height = 0.075)
    pLabel = text(text = 'momentum', pos=ball.pos, color=color.blue, billboard=True, emissive=True, height = 0.075)
    
    while dist >= 0.05:
        
        rate(100)
        airResis = (-1/2) * rho * A * C * (mag(ball.p/ball.m))**2 * norm(ball.p/ball.m)
        F = (ball.m * g) + airResis
        ball.p = ball.p + F * dt
        airResisVec.pos = gVector.pos = pVector.pos = light.pos = ball.pos = ball.pos + ball.p * dt/ball.m
        
        textUpdate(gLabel, gVector)
        textUpdate(arLabel, airResisVec)
        textUpdate(pLabel, pVector)
        
        pVector.axis = norm(ball.p) * 0.25
        airResisVec.axis = norm(airResis) * 0.25
        
        t = t + dt
        dist = ball.pos.y - base.pos.y
        gp.plot(t, ball.pos.y)
        gv.plot(t, ball.p.y/ball.m)
        ga.plot(t, g.y + airResis.y)
        
    

    running = False
'''     
def reset():
    for obj in scene.objects:
        if obj == base:
            obj.visible = True
        else:
            obj.visible = False
            del obj
    for light in scene.lights:
        if isinstance(light, local_light):
            light.visible = False
            del light
    initVectors()
'''
'''
def resetGraph():
    gx.delete()
    gv.delete()
    ga.delete()
    
'''
scene.caption = "Set launch height:                                     code sometimes breaks after you mess with the graph\n"

def setHeight(h):
    wt.text = '{:1.2f}'.format(h.value)

sl = slider(min=0, max=1, value=0, length=220, bind=setHeight, right=15)

wt = wtext(text='{:1.2f}'.format(sl.value))

scene.append_to_caption(' meters\n')

scene.append_to_caption("Set launch magnitude: \n")

def setMag(m):
    wt2.text = '{:1.2f}'.format(m.value)

sl2 = slider(min=0, max=10, value=5, length=220, bind=setMag, right=15)

wt2 = wtext(text='{:1.2f}'.format(sl2.value))

scene.append_to_caption(' meters/s\n')

scene.append_to_caption("Set launch angle: \n")

def setAng(a):
    wt3.text = '{:1.2f}'.format(a.value)

sl3 = slider(min=0, max=90, value=45, length=220, bind=setAng, right=15)

wt3 = wtext(text='{:1.2f}'.format(sl3.value))

scene.append_to_caption(' degrees \n')

scene.append_to_caption("Set Air Density: \n")

def setAr(a):
    wt4.text = '{:1.2f}'.format(a.value)

sl4 = slider(min=0, max=10, value=1.2, length=220, bind=setAr, right=15)

wt4 = wtext(text='{:1.2f}'.format(sl4.value))

scene.append_to_caption(' kg/m^3 \n\n')




height = sl.value
magnitude = sl2.value
angle = sl3.value


def initVectors():
    #heightInit = arrow(radius = 0.02, pos = vec(-1.5, 0, 0), color = color.red)
    #magInit = arrow(radius = 0.02, pos = vec(-1.5, 0, 0), color = color.blue)
    angleInit = arrow(radius = 0.02, pos = vec(-1.5, 0, 0), color = color.yellow)
    global angleInit
    '''
    while not running:
        rate(60)
        
        #heightInit.axis = norm(vec(0, height, 0) * 0.25)
        #magInit.axis = norm(vec(magnitude, 0, 0) * 0.25)
        angleInit.axis = norm(vec(cos(sl3.value * pi/180), sin(sl3.value * pi/180), 0) )
    '''
    

def launchArgs():
    launch(sl.value, sl2.value, sl3.value, sl4.value)


        

button(bind = launchArgs, text = "Launch")
scene.append_to_caption('\n\n\n')
#button(bind = resetGraph, text = "Clear Graph")
#button(bind = reset, text = "reset")

initVectors()

while True:
    if not running:
        rate(100)
        angleInit.axis = (norm(vec(cos(sl3.value * pi/180) , sin(sl3.value * pi/180), 0)) * 0.5 )
        angleInit.length = sl2.value * 0.1
        angleInit.pos =  vec(-1.5, sl.value + 0.05, 0)
