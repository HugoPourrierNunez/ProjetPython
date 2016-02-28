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
        
    def getTuple(self):
        return (self.r,self.g,self.b)


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
    AMBIANTE=1
    DIFFUSE=2
    SPECULAIRE=3
    def __init__(self,point,color=Color(),intensite=1, mode=AMBIANTE):
        self.point=point
        self.color=color
        self.mode=mode
        self.intensite=intensite

class Sphere:
    def __init__(self,point,rayon,color,ambiante=1,diffuse=1,speculaire=1,brillance=1):
        self.point=point
        self.rayon=rayon
        self.color=color
        self.ambiante = ambiante
        self.diffuse = diffuse
        self.speculaire=speculaire
        self.brillance=brillance

class Scene:
    
    def __init__(self,camera):
        self.camera=camera
        self.tabLight=[]
        self.tabSphere=[]
        self.buffer=[(0,0,0)]*self.camera.screen_width*self.camera.screen_height
        self.image = Image.new("RGB", (self.camera.screen_width, self.camera.screen_height))
        self.buffer = self.image.load()
        for x in range(self.camera.screen_width):
            for y in range(self.camera.screen_height):
                self.buffer[x,y]=(0,0,0)
                     
    def __add__(self, element):
        if isinstance(element,Light):
            self.tabLight.append(element)
        elif isinstance(element,Sphere):
            self.tabSphere.append(element)

    def process(self):
        for light in self.tabLight:
            if light.mode == Light.AMBIANTE:
                direction=Vector(0,1,0)
                for i in range(0,self.camera.screen_width):
                    for j in range(0,self.camera.screen_height):
                        #direction=Vector(i-position.x,j-position.y,self.camera.focale-position.z)
                        #print("x=",direction.x,"y=",direction.y,"z=",direction.z)
                        position=Vector(i,j,0)
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
                                if pointMin==False:
                                    normeMin=sqrt((p.x-position.x)**2+(p.y-position.y)**2+(p.z-position.z)**2)
                                    pointMin=p
                                    colorMin=sphere.color
                                else:
                                    norme=sqrt((p.x-position.x)**2+(p.y-position.y)**2+(p.z-position.z)**2)
                                    if norme<normeMin:
                                        normeMin=norme
                                        pointMin=p
                                        colorMin=sphere.color
                        if pointMin!=False:
                            self.buffer[i,j]=colorMin.getTuple()
            
    def process2(self):
        test=1
                    
    def draw(self,name):
        file=open(name,'w')
        self.image.save(file, "JPEG")
        file.close()
                    
        

    
scene = Scene(Camera(500,500,500,500,1000))
scene+Sphere(Point(250,250,0), 50, Color(0,0,255))
scene+Sphere(Point(200,250,10), 100, Color(255,0,0))
scene+Light(Point(10,20,5))
scene.process()
scene.draw("test2.jpg")

