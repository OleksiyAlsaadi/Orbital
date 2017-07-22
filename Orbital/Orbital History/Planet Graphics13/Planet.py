import pygame, sys
import time
import random
import math
from math import *
from pygame.locals import *
pygame.init()
fps=48

WIDTH=int(800)
HEIGHT=int(600)
screen=pygame.display.set_mode((WIDTH,HEIGHT))
Clock=pygame.time.Clock()

#Load Files
ground1=pygame.image.load("Images\\ground1.png").convert_alpha()
ground2=pygame.image.load("Images\\ground2.png").convert_alpha()
circle=pygame.image.load("Images\\circle.png").convert_alpha()
blue_sky=pygame.image.load("Images\\blue_sky.png").convert_alpha()
background=pygame.image.load("Images\\background.png").convert_alpha()

#Colors
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
ORANGE=(234,94,0)

#Landscape
size=38
rotation=[]
landy=[]
w=[]
h=[]
spin=[]
for n in range(10):
    w.append(n); w[n]=random.randint(0,10000)
    h.append(n); h[n]=random.randint(0,10000)
    spin.append(n); spin[n]=random.randint(-500,500)/100000
    
    rotation.append(n); rotation[n]=0
    landy.append(n); landy[n]=random.randint(50,200)
    if (landy[n]>100): landy[n]=random.randint(150,190)


#Rocketship
rx=w[0]-1; ry=h[0]-10 #x and y coordinates
rs=20 #rocket size
rrot=0 #rocket rotation
rw=1 #rocket width
rd=0 #holding d or not
ra=0 #holding a or not
engine=0 #holding w or not (engine on or not)
dx=0 #x rocket movement
dy=0 #y rocket movement
landed=1 #if landed on planet
crashed=0 #if crashed

explodex=[] #crash particles
explodey=[]
explodedx=[]
explodedy=[]
for n in range(30):
    explodex.append(n); explodex[n]=WIDTH/2
    explodey.append(n); explodey[n]=HEIGHT/2
    explodedx.append(n); explodedx[n]=random.randint(-80,80)/100
    explodedy.append(n); explodedy[n]=random.randint(-80,80)/100




def displaySky():
    global w,h

    #Background Stars
    backgroundsize=pygame.transform.scale(background, (WIDTH,HEIGHT))
    screen.blit(backgroundsize,(0,0))

    for n in range(10):
        if (w[n]>rx-WIDTH and w[n]<rx+WIDTH and h[n]>ry-HEIGHT and h[n]<ry+HEIGHT):
            #Sky
            circlesize=pygame.transform.scale(blue_sky,(landy[n]*2+500+100,landy[n]*2+500+100))
            rect=circlesize.get_rect()
            screen.blit(circlesize,(w[n]-rect[2]/2-rx+WIDTH/2,h[n]-rect[3]/2-ry+HEIGHT/2))    

            #Center Dark Circle
            circlesize=pygame.transform.scale(circle,(landy[n]*2,landy[n]*2))
            rect=circlesize.get_rect()
            screen.blit(circlesize,(w[n]-rect[2]/2-rx+WIDTH/2,h[n]-rect[3]/2-ry+HEIGHT/2))

def displayPlanet():
    global rotation
    global w,h

    for nn in range(10):
        if (w[nn]>rx-WIDTH and w[nn]<rx+WIDTH and h[nn]>ry-HEIGHT and h[nn]<ry+HEIGHT):
            for n in range(-1,size-1):
                angle=((3.14*2)/size)*n+rotation[nn]
                angle2=((3.14*2)/size)*(n+1)+rotation[nn]
                #Display Ground
                if (landy[nn]<=100): ground=ground1
                if (landy[nn]>100): ground=ground2
                oldCenter=ground.get_size()
                groundRot=pygame.transform.rotate(ground,angle*57.3)
                rect=groundRot.get_rect()
                rect.center=oldCenter
                screen.blit(groundRot,(w[nn]+landy[nn]*sin(angle)+rect[0]-oldCenter[0]-rx+WIDTH/2,h[nn]+landy[nn]*cos(angle)+rect[1]-oldCenter[1]-ry+HEIGHT/2))
                
        rotation[nn]=rotation[nn]+spin[nn] #Rotate Planet
        if (rotation[nn]>=3.14*2): rotation[nn]=0

def displayRocketship():
    pygame.draw.line(screen, WHITE, (WIDTH/2+rs*cos(rrot-3.14/2),HEIGHT/2+rs*sin(rrot-3.14/2)), (WIDTH/2+rs*cos(rrot+rw),HEIGHT/2+rs*sin(rrot+rw)))
    pygame.draw.line(screen, WHITE, (WIDTH/2+rs*cos(rrot-3.14/2),HEIGHT/2+rs*sin(rrot-3.14/2)), (WIDTH/2+rs*cos(rrot-3.14-rw),HEIGHT/2+rs*sin(rrot-3.14-rw)))
    pygame.draw.line(screen, WHITE, (WIDTH/2+rs*cos(rrot+rw),HEIGHT/2+rs*sin(rrot+rw)), (WIDTH/2+rs*cos(rrot-3.14-rw),HEIGHT/2+rs*sin(rrot-3.14-rw)))
    if (engine==1):
        pygame.draw.line(screen, ORANGE, (WIDTH/2+rs*2*cos(rrot+3.14/2),HEIGHT/2+rs*2*sin(rrot+3.14/2)), (WIDTH/2+rs*.9*cos(rrot+rw*1.2),HEIGHT/2+rs*.9*sin(rrot+rw*1.2)))
        pygame.draw.line(screen, ORANGE, (WIDTH/2+rs*2*cos(rrot+3.14/2),HEIGHT/2+rs*2*sin(rrot+3.14/2)), (WIDTH/2+rs*.9*cos(rrot-3.14-rw*1.2),HEIGHT/2+rs*.9*sin(rrot-3.14-rw*1.2)))
        pygame.draw.line(screen, ORANGE, (WIDTH/2+rs*.9*cos(rrot+rw*1.2),HEIGHT/2+rs*.9*sin(rrot+rw*1.2)), (WIDTH/2+rs*.9*cos(rrot-3.14-rw*1.2),HEIGHT/2+rs*.9*sin(rrot-3.14-rw*1.2)))       

def crashedRocketship():
    for n in range(30):
        if (explodex[n]==WIDTH/2): explodex[n]=WIDTH/2+explodedx[n]
        if (explodey[n]==HEIGHT/2): explodey[n]=HEIGHT/2+explodedy[n]
        explodex[n]=explodex[n]+explodedx[n]
        explodey[n]=explodey[n]+explodedy[n]
        explodedx[n]=explodedx[n]*.995
        explodedy[n]=explodedy[n]*.995
        pygame.draw.line(screen, WHITE, (explodex[n],explodey[n]), (explodex[n]+explodedx[n]*25,explodey[n]+explodedy[n]*25))

def controlRocketship():
    global rrot
    global dy,dx
    global rx,ry
    global landed, crashed

    if (landed==0): #Rotating
        if (rd==1): rrot=rrot+0.03
        if (ra==1): rrot=rrot-0.03
    if (rrot>=3.14 or rrot<=-3.14): rrot=-rrot
    if (engine==1): #Movement
        dy=dy-sin(rrot+3.14/2)*0.06
        dx=dx-cos(rrot+3.14/2)*0.06
        if (dy>5): dy=dy-0.06
        if (dy<-5): dy=dy+0.06

    for n in range(10):
        if (w[n]>rx-WIDTH and w[n]<rx+WIDTH and h[n]>ry-HEIGHT and h[n]<ry+HEIGHT):
            a=w[n]-rx #Gravity
            b=h[n]-ry
            c=(a*a+b*b)**.5
            if (c<landy[n]+500 and c>=landy[n]+250):
                d=atan(b/a); aa=cos(d)*.3; bb=sin(d)*.3
                if (c<landy[n]+350): d=atan(b/a); aa=cos(d)*.7; bb=sin(d)*.7
                if (a>0): dx=dx+aa/30; dy=dy+bb/30
                if (a<0): dx=dx-aa/30; dy=dy-bb/30      
            if (c<landy[n]+250):
                d=atan(b/a); aa=cos(d)*1.3; bb=sin(d)*1.3
                if (a>0): dx=dx+aa/30; dy=dy+bb/30
                if (a<0): dx=dx-aa/30; dy=dy-bb/30
                if (dx>0): dx=dx-.01
                if (dx<0): dx=dx+.01
                if (dy>0): dy=dy-.01
                if (dy<0): dy=dy+.01
                d=d-spin[n]
                rrot=rrot-spin[n]
                if (a<0): rx=w[n]+cos(d)*c; ry=h[n]+sin(d)*c
                if (a>=0): rx=w[n]-cos(d)*c; ry=h[n]-sin(d)*c
                
            #Planet Collision
            if (c<landy[n]+38): #Crashes
                d=atan(b/a)
                d=d-spin[n]
                ang=abs(rrot-d)
                if (ang>3.14): ang=ang-3.14
                if (abs(dx)+abs(dy)>4 or ang<1.57-.8 or ang>1.57+.8): crashed=1
                if (abs(dx)+abs(dy)>.7): dx=-dx; dy=-dy
                
                if (abs(dx)+abs(dy)<=.7):
                    if ((c<landy[n]+38) and (engine==0 or landed==0)): #Landed
                        landed=1
                        dx=0; dy=0
                        if (a>=0):
                            if (ang<1.57-.05): rrot=rrot-.03
                            if (ang>1.57+.05): rrot=rrot+.03
                        if (a<0):
                            if (ang<1.57-.05): rrot=rrot+.03
                            if (ang>1.57+.05): rrot=rrot-.03
                        if (a<0): rx=w[n]+cos(d)*(landy[n]+18+20); ry=h[n]+sin(d)*(landy[n]+18+20)
                        if (a>=0): rx=w[n]-cos(d)*(landy[n]+18+20); ry=h[n]-sin(d)*(landy[n]+18+20)     
            if (c>landy[n]+38): landed=0

    rx=rx+dx
    ry=ry+dy    














mainloop=True 
while mainloop:
    
    Clock.tick(fps)
    screen.fill(BLACK)

    if (crashed==0): controlRocketship() #Control Rocketship
    displaySky() #Display Sky and Center
    if (crashed==0): displayRocketship() #Display Rocketship
    displayPlanet() #Display Planet
    if (crashed==1): crashedRocketship() #Crashed Rocketship

    for event in pygame.event.get():
        
        if (event.type==KEYDOWN): #Press Keys
            if (event.key==pygame.K_d): rd=1
            if (event.key==pygame.K_a): ra=1
            if (event.key==pygame.K_w): engine=1
        elif (event.type==KEYUP):
            if (event.key==pygame.K_d): rd=0
            if (event.key==pygame.K_a): ra=0
            if (event.key==pygame.K_w): engine=0

        elif (event.type==QUIT): #Quitting
            mainloop=False

    pygame.display.set_caption("FPS: "+str(int(Clock.get_fps()))+" ")
    pygame.display.flip()
    
pygame.quit()
