class Point:

    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z
        
class Vector:

    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z

class Color:

    def __init__(self,r=0,g=0,b=0):
        self.b=b
        self.r=r
        self.g=g


class Ray:

    def __init__(self,point,vector):
        self.point=point
        self.vector=vector

class Camera:
    def __init__(self,screen_width,screen_height,width,height,focale):
        self.screen_width=screen_width
        self.screen_height=screen_height
        self.width=width
        self.height=height
        self.focale=focale

class Light:
    def __init__(self,point,color):
        self.point=point
        self.color=color

class Sphere:
    def __init__(self,point,rayon,color,coef=1):
        self.point=point
        self.rayon=rayon
        self.color=color
        self.coef=coef

class Scene:
    def __init__(self,camera):
        self.camera=camera
        self.tabLight=[]
        self.tabSphere=[]
        self.buffer=([0]*self.camera.screen_width,[0]*self.camera.screen_height)

    def __add__(self, element):
        if isinstance(element,Light):
            self.tabLight.append(element)
        elif isinstance(element,Sphere):
            self.tabSphere.append(element)

    def process(self):
        for i in range(0,self.camera.screen_width):
            for j in range(0.self.camera.screen_height):
                v=Vector(0,1,0)
        

    
scene = Scene(Camera(1,1,1,1,1))
sphere = Sphere(0,0,0)
scene+1
print(scene.buffer[0][0])

