from math import *
from PIL import Image

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
        self.buffer=[(0,0,0)]*self.camera.screen_width*self.camera.screen_height
                     
    def __add__(self, element):
        if isinstance(element,Light):
            self.tabLight.append(element)
        elif isinstance(element,Sphere):
            self.tabSphere.append(element)

    def process(self):
        direction=Vector(0,1,0)
        for i in range(0,self.camera.screen_width):
            for j in range(0,self.camera.screen_height):
                position=Point(i,j,0)
                pointMin = False
                colorMin = False
                for sphere in self.tabSphere:
                    find=False
                    a = direction.x**2 + direction.y**2 + direction.y**2
                    b= 2*(direction.x*(position.x-sphere.point.x)+direction.y*(position.y-sphere.point.y)+direction.z*(position.z-sphere.point.z))
                    c = ((sphere.point.x-position.x)**2+(sphere.point.y-position.y)**2+(sphere.point.z-position.z)**2)-sphere.rayon**2
                    det = b**2-(4*a*c)
                    if det>0:
                        t1 = (-b+sqrt(det))/(2*a)
                        t2 = (-b-sqrt(det))/(2*a)
                        if abs(t1)>abs(t2):
                            t1=t2
                        find=t1
                    elif det==0:
                        find=-b/(2*a)
                    if find!=False:
                        p = Point(((position.x+direction.x*find)-sphere.point.x)**2, ((position.y+direction.y*find)-sphere.point.y)**2,((position.z+direction.z*find)-sphere.point.z)**2)
                        pointMin=p
                        colorMin=sphere.color
                if pointMin!=False:
                    self.buffer[i*self.camera.screen_width+j]=(colorMin.r,colorMin.g,colorMin.b)
                    
    def draw(self):
        f=open("test2.jpg",'w')
        image = Image.new("RGB", (self.camera.screen_width, self.camera.screen_height))
        pix = image.load()
        for x in range(self.camera.screen_width):
            for y in range(self.camera.screen_height):
                pix[x,y]=self.buffer[x*self.camera.screen_width+y]
        image.save(f, "JPEG")
        f.close()
                    
        

    
scene = Scene(Camera(500,500,500,500,1))
sphere = Sphere(Point(200,200,0), 50, Color(255,0,0))
scene+sphere
scene.process()
scene.draw()

