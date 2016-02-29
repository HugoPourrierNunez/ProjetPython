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

    def fromPoint(p1,p2,norm=False):
        x=p2.x-p1.x
        y=p2.y-p1.y
        z=p2.z-p1.z
        if norm:
            n=p1.norme(p2)
            x/=n
            y/=n
            z/=n
        return Vector(x,y,z)

    def myprint(self):
        print("x=",self.x," y=",self.y," z=",self.z)

    def __add__(self, vB):
        return Vector(self.x+vB.x,self.y+vB.y,self.z+vB.z) 
    
    def __sub__(self, vB):
        return Vector(self.x-vB.x,self.y-vB.y,self.z-vB.z) 
    
    def __mul__(self, c): 
        if isinstance(c,Vector):
            return  self.x*c.x+self.y*c.y+self.z*c.z  
        else:
            return Vector(c*self.x,c*self.y,c*self.z) 
        
    def __div__(self, c):
        return Vector(self.x/c, self.y/c,self.z/c)  

class Color:

    def __init__(self,r=0,g=0,b=0):
        self.b=b
        self.r=r
        self.g=g
        
    def getTuple(self):
        return (self.r,self.g,self.b)

    def addition(t,c,intensite=1):
        return (int(t[0]+c.r*intensite),int(t[1]+c.g*intensite),int(t[2]+c.b*intensite))

    def mixe(self,c):
        return Color(int((self.r+c.r)/2),int((self.g+c.g)/2),int((self.b+c.b)/2))

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
    PHONG=4
    def __init__(self,point,color=Color(255,255,255),intensite=1, mode=AMBIANTE):
        self.point=point
        self.color=color
        self.mode=mode
        self.intensite=intensite

class Sphere:
    def __init__(self,point,rayon,color,ambiante=.2,diffuse=1,speculaire=1,brillance=20):
        self.point=point
        self.rayon=rayon
        self.color=color
        self.ambiante = ambiante
        self.diffuse = diffuse
        self.speculaire=speculaire
        self.brillance=brillance

    def colision(self,v,p):
        point=False
        a = v.x**2 + v.y**2 + v.z**2
        b= 2*(v.x*(p.x-self.point.x)+v.y*(p.y-self.point.y)+v.z*(p.z-self.point.z))
        c = ((self.point.x-p.x)**2+(self.point.y-p.y)**2+(self.point.z-p.z)**2)-self.rayon**2
        #b= 2*(v.x*(p.x)+v.y*(p.y)+v.z*(p.z))
        #c = ((p.x)**2+(p.y)**2+(p.z)**2)-self.rayon**2
        det = b**2-(4*a*c)
        if det>0:
            t1 = (-b+sqrt(det))/(2*a)
            p1=Point(v.x*t1+p.x,v.y*t1+p.y,v.z*t1+p.z)
            
            t2 = (-b-sqrt(det))/(2*a)
            p2=Point(v.x*t2+p.x,v.y*t2+p.y,v.z*t2+p.z)

            if p1.norme(p)>p2.norme(p):
                point=p2
            else:
                point=p1
        elif det==0:
            t=-b/(2*a)
            point=Point(v.x*t+p.x,v.y*t+p.y,v.z*t+p.z)
        return point

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
        direction=Vector(0,0,1)
        maxI=0
        for i in range(0,self.camera.screen_width):
            for j in range(0,self.camera.screen_height):
                position=Vector(i,j,0)
                pointMin = False
                colorMin = False
                for sphere in self.tabSphere:
                    p=sphere.colision(direction,position)
                    if p!=False:
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
                    p=pointMin
                    for light in self.tabLight:
                        
                        if light.mode == Light.AMBIANTE or light.mode == Light.PHONG:
                            self.buffer[i,j]=Color.addition(self.buffer[i,j],sphereMin.color,sphereMin.ambiante*light.intensite)

                        if light.mode!= Light.AMBIANTE :
                            L=Vector.fromPoint(p,light.point,True)
                            N=Vector.fromPoint(sphereMin.point,p,True)
                            
                            if L*N>0:
                                directLight=True
                                for sphere in self.tabSphere:
                                    if sphere != sphereMin:
                                        col=sphere.colision(L,p)
                                        if col!=False and p.norme(col)<p.norme(light.point) and N*Vector.fromPoint(p,col)>0:
                                            directLight=False
                                            break
                                
                                if directLight:
                                    
                                    if light.mode == Light.DIFFUSE or light.mode == Light.PHONG :
                                        intensite=L*N*sphereMin.diffuse*light.intensite
                                        if intensite>0:
                                            self.buffer[i,j]=Color.addition(self.buffer[i,j],sphereMin.color,intensite)
                                        
                                    if light.mode == Light.SPECULAIRE or light.mode == Light.PHONG:
                                        V=Vector.fromPoint(p,position,True)
                                        R=N*2*(N*L)-L
                                        intensite=(R*V)**sphereMin.brillance*sphereMin.speculaire*light.intensite
                                        if intensite>0:
                                            self.buffer[i,j]=Color.addition(self.buffer[i,j],light.color,intensite)


                                          
    def draw(self,name):
        file=open(name,'w')
        self.image.save(file, "JPEG")
        file.close()
                    
        

    
scene = Scene(Camera(500,500,500,500,1))

scene+Sphere(Point(350,250,350), 100, Color(255,0,0))
scene+Sphere(Point(250,200,250), 50, Color(0,0,255))
scene+Sphere(Point(150,245,150), 20, Color(0,255,0))
scene+Sphere(Point(200,356,142), 70, Color(255,0,0))
scene+Sphere(Point(325,6,35), 114, Color(0,0,255))
scene+Sphere(Point(10,150,15), 28, Color(0,255,0))


#scene+Light(Point(0,0,0), mode=Light.SPECULAIRE)
#scene+Light(Point(0,0,0), mode=Light.DIFFUSE)
#scene+Light(Point(0,0,0))

scene+Light(Point(0,250,0), mode=Light.PHONG)
scene+Light(Point(0,0,0), mode=Light.PHONG, intensite=0.5)
#scene+Light(Point(500,500,0), mode=Light.PHONG)

scene.process()
scene.draw("test2.jpg")



