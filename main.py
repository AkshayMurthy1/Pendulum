import math
import pygame
import sys
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import asyncio
pmr = 90 #1 meter = pmr pixels
gpixels = 9.8*pmr

pygame.init()
width = 1200
height = 800
iXY = (width/2,height/2)
screen = pygame.display.set_mode((width,height))

#time tracker
clock = pygame.time.Clock()

#pygame.font.init()
#font = pygame.font.SysFont(None,25)
time_txt = TextBox(screen,0,0,150,30,fontSize = 15)
per_txt = TextBox(screen,0,time_txt.getHeight(),150,30,fontSize = 15)
angle_txt = TextBox(screen,0,per_txt.getY()+per_txt.getHeight(),150,30,fontSize = 15)
vel_txt = TextBox(screen,0,angle_txt.getY()+angle_txt.getHeight(),180,30,fontSize = 15)
disp_txt = TextBox(screen,0,vel_txt.getY()+vel_txt.getHeight(),210,30,fontSize = 15)
time_txt.disable()
per_txt.disable()
angle_txt.disable()
vel_txt.disable()
disp_txt.disable()

length = 2
ampr = .5

length_slider = Slider(screen,25,disp_txt.getY()+disp_txt.getHeight()*2,60,40,min = .5, max = 10, step = .01, colour = (255,25,25),handleColour = (25,255,25),intial = 2, handleRadius = 15, curved = True)
length_txt = TextBox(screen,length_slider.getX()-20,length_slider.getY()+40,120,40,fontSize = 15)
length_txt.disable()
amp_slider = Slider(screen,25,length_slider.getY()+disp_txt.getHeight()*3,60,40,min = 0, max = 2, step = .01, colour = (255,25,25),handleColour = (25,255,25),intial = 2, handleRadius = 15, curved = True,)
amp_txt = TextBox(screen,amp_slider.getX()-20,amp_slider.getY()+40,120,40,fontSize = 15)
amp_txt.disable()



frames = 0
def restart():
    global frames
    frames = 0

restart_but = Button(screen,20,amp_txt.getY()+amp_txt.getHeight()*2,50,50,text = 'Restart', fontSize = 15, margin = 20, inactiveColour = (0,200,20),hoverColour=(150,25,25),pressedColour=(255,0,0), radius = 30, onClick = restart)

def get_disp(t, A, length,g):
    return A*math.cos(math.sqrt(g/length)*t)
def get_init_angle(A,length):
    return math.acos(1-(A**2/(2*length**2.0)))
def get_angle(t,A,length,g):
    T = 2*math.pi*math.sqrt(length/g)
    try: 
        init_angle = get_init_angle(A,length)
    except:
        sys.exit(f"How can the ball possible be {A/pmr} meters away from its center if the length is only {length/pmr} meters ")
    return (init_angle*math.cos((2*math.pi/T)*t))

def get_pos_change(angle,length) -> tuple:
    return (length*math.sin(angle), length-length*math.cos(angle))
def get_velocity(angle,init_angle,length,g):
    return math.sqrt(2*g*length*(math.cos(angle)-math.cos(init_angle)))

run = True
async def main():
    global run,gpixels,length,ampr,pmr,width,height,iXY,frames
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            
        screen.fill((0,0,0))
        pygame_widgets.update(events)
        #pygame.draw.circle(screen,(255,255,255),(width/2,0),10)
        if length!=length_slider.getValue():
            length = length_slider.getValue()
            iXY = (width/2,height/4+length*pmr)
        elif ampr!=amp_slider.getValue():
            ampr = amp_slider.getValue()
            iXY = (width/2,height/4+length*pmr)
        amp = ampr*length #in meters
        lengthpix = length*pmr
        apix = amp*pmr
        if frames==0:
            XY = iXY
        
        
        angle = get_angle(frames/50,apix,lengthpix,gpixels)
        pos_change = (get_pos_change(angle,lengthpix))
        XY = (iXY[0]+pos_change[0],iXY[1]-pos_change[1])
        pygame.draw.circle(screen,(255,0,0),XY,20)
        pygame.draw.line(screen,(0,255,0),(width/2,height/4),XY)
        
        time_txt.setText(f"Time: {int((frames/50)*10)/10}")
        period = 2*math.pi*math.sqrt(lengthpix/gpixels)
        per_txt.setText(f"Time/Period: {int((frames/50%period)*10)/10}/{int(period*10)/10}")
        max_angle = get_init_angle(apix,lengthpix)
        angle_txt.setText(f"Angle: {int(angle*180/math.pi*10)/10}°/{int(max_angle*180/math.pi*10)/10}°")

        velocity = get_velocity(angle,max_angle,length,gpixels/pmr)
        vel_txt.setText(f"Tangential velocity: {int(velocity*10)/10} m/s")

        disp = get_disp(frames/50,amp,length,gpixels/pmr)
        disp_txt.setText(f"Absolute Displacement: {int(disp*10)/10} m")
        length_txt.setText(f"Length: {length}m")
        amp_txt.setText(f"Amplitude: {amp}m")
        
        pygame.display.update()
        clock.tick(50)
        frames+=1
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())