from math import *
from PIL import Image

class Point:

    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z

    def norme(self,p):
        return sqrt((p.x-self.x)**2+(p.y-self.y)**2+(p.z-self.z)**2)
        
class Vector:

    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z

    def myprint(self):
        print("x=",self.x," y=",self.y," z=",self.z)

    def scalaire(self,v):
        return self.x*v.x+self.y*v.y+self.z*v.z

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
        direction=Vector(0,1,0)
        maxI=0
        for i in range(0,self.camera.screen_width):
            for j in range(0,self.camera.screen_height):
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
                        if t1>t2:
                            t1=t2
                        find=t1
                    elif det==0:
                        find=-b/(2*a)
                    if find!=False:
                        p=Point(direction.x*find+position.x,direction.y*find+position.y,direction.z*find+position.z)
                        if pointMin==False:
                            normeMin=p.norme(position)
                            pointMin=p
                            sphereMin=sphere
                        else:
                            norme=p.norme(position)
                            if norme<normeMin:
                                normeMin=norme
                                pointMin=p
                                sphereMin=sphere

                if pointMin!=False:
                    
                    for light in self.tabLight:
                        
                        if light.mode == Light.DIFFUSE:
                            
                            normeL=p.norme(light.point)
                            
                            L=Vector((light.point.x-p.x)/normeL,(light.point.y-p.y)/normeL,(light.point.z-p.z)/normeL)
                            N=Vector((p.x-sphereMin.point.x)/sphereMin.rayon,(p.y-sphereMin.point.y)/sphereMin.rayon,(p.z-sphereMin.point.z)/sphereMin.rayon)
                            
                            intensite=L.scalaire(N)*sphereMin.diffuse*light.intensite
                            if intensite>maxI:
                                maxI=intensite
                            if intensite>0:
                                self.buffer[i,j]=(self.buffer[i,j][0]+int(sphereMin.color.r*intensite),self.buffer[i,j][1]+int(sphereMin.color.g*sphereMin.diffuse*intensite),self.buffer[i,j][2]+int(sphereMin.color.b*sphereMin.diffuse*intensite))
                            
                        if light.mode == Light.AMBIANTE:
                            self.buffer[i,j]=(self.buffer[i,j][0]+int(sphereMin.color.r*sphereMin.ambiante),self.buffer[i,j][1]+int(sphereMin.color.g*sphereMin.ambiante),self.buffer[i,j][2]+int(sphereMin.color.b*sphereMin.ambiante))

                        if light.mode == Light.SPECULAIRE:
                            test=1
                        

        print("maxI",maxI)
        

            
    def process2(self):
        test=1
                    
    def draw(self,name):
        file=open(name,'w')
        self.image.save(file, "JPEG")
        file.close()
                    
        

    
scene = Scene(Camera(500,500,500,500,1000))
scene+Sphere(Point(250,250,-25), 50, Color(0,0,255),ambiante=.2)
scene+Sphere(Point(200,250,10), 100, Color(255,0,0),ambiante=.2)
scene+Light(Point(0,0,0), mode=Light.DIFFUSE)
scene+Light(Point(0,0,0))
scene.process()
scene.draw("test2.jpg")

