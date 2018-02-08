# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 11:54:52 2018

@author: Ari
"""


import numpy as np
import matplotlib.pyplot as plt # https://matplotlib.org/examples/index.html
import matplotlib.animation as animation
import random
import wave
import sys
import struct
import pyaudio

class Orbits:
    """
    Orbits class calculates schwarzschild planar orbits around black hole
    
    """

#   Open audio file ***********************************************************
    
CHUNK = 1024

# validation. If a wave file hasn't been specified, exit.
#if len(sys.argv) < 2:
#    print("Plays a wave file.\n\nUsage: %s full send.wav" % sys.argv[0])
#    sys.exit(-1)
    
wf = wave.open('C:/Users/Ari/Documents/Python Scripts/full send.wav', 'rb')



# instantiate PyAudio (1)
p = pyaudio.Pyaudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data
data = wf.readframes(CHUNK)

# play stream (3)
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)




    def __init__(self):
               
        init_state = [[100,100], [0]] # initial conditions [R, PHI]
        GM = 1 # comsmological constant
        U = 1 # initial angular speed
        L = (init_state[0][0]**2) * U # constant angular momentum
        dt = (2*np.pi*U) / 500 # time step ensuring smooth steps
        self.dt = dt
        init_state[1].append(+(.5*U*dt)) # first PHI value
        self.state = init_state
        self.time_elapsed = 2 # starts on third time step / counts steps
        self.real_time = 2*dt # counts real time elapsed
        self.params = (GM, L, dt)
        
    def calcR(self):
        """ Compute radial value at time step dt """
        (GM, L, dt) = self.params
        
        past_R = self.state[0][self.time_elapsed-2]
        curr_R = self.state[0][self.time_elapsed-1]
    
        R = 2*curr_R - past_R + (dt**2 * (-(GM/(curr_R**2)) + ((L**2)/(curr_R**3)) - ((3*GM*(L**2))/(curr_R**4))))
        return R
    
    def calcPHI(self):
        """ Compute phi value at time step dt """
        (GM, L, dt) = self.params
        
        curr_PHI = self.state[1][self.time_elapsed-1]
        past_R = self.state[0][self.time_elapsed-1]
        curr_R = self.state[0][self.time_elapsed]
        PHI = curr_PHI + (dt * (L/(.5*(curr_R + past_R))**2))
        return PHI
    
    def position(self):
        
        return (self.state[0][self.time_elapsed-1], self.state[1][self.time_elapsed-1])
#       return (self.state[0][:], self.state[1][:])
    
    def step(self):
        """execute one time step of length dt and update state"""
        self.state[0].append(self.calcR())
        self.state[1].append(self.calcPHI())
      
        self.time_elapsed += 1
        self.real_time += self.dt
        
    def pol2cart(rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        
        return(x, y)
        
        
# *****************************************************************************


# qualitative test of algorithm
#orbit = Orbits()
#for x in range(0,11):
#    orbit.step()
#   # print('%d' % x)
#print(orbit.state)
#print(orbit.time_elapsed)


#******************************************************************************

        
# set up initial state and variables
orbit = Orbits()        
dt = orbit.dt


# generate data before animation
#for i in range(0,10):
#    orbit.step()

#------------------------------------------------------------
    
    
    
# set up figure and animation
fig = plt.figure()
ax = fig.add_subplot(111,projection= 'polar', facecolor = 'black')
ax.set_title("Particle Orbits in Schwarszchild Space-Time")
ax.set_rlim(-100, 25)
#ax.set_rticks([25,50,75,100])
line, = ax.plot([],[],'blueviolet', lw=.5,animated=True)
circle = plt.Circle(5, facecolor= 'deepskyblue')
#hole = plt.Circle((0,0), 3, facecolor= 'black', edgecolor= 'white' )



def init():
    """initialize animation"""
    line.set_data([], [])
    ax.add_patch(circle)
#    ax.add_patch(hole)
    return [line, circle]

def animate(i):
    """perform animation step"""
    global orbit, dt
    orbit.step()

    
    rho = orbit.state[0][i]     # set data for new segment of line to be drawn tracing orbit
    phi = orbit.state[1][i]   
    l = np.linspace(0,100,500)
    w = np.arange(0,1,.01)
    theta = 2 * np.pi * w
    x= rho*l
    y= phi
    line.set_data([x,y])  
    circle.center = (1-i,1-i)
    
    if (orbit.time_elapsed % 10 == 0):    # make pretty colors
        r = random.randint(0,10)*.100
        g = random.randint(0,10)*.100
        b = random.randint(0,10)*.100
       
        color = (r,g,b)
        line.set_color(color)
        
    return [line, circle]
        
  

# choose the interval based on dt and the time to animate one step
from time import time
t0 = time()
animate(0)
t1 = time()
interval = 1000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig, animate, frames=1000,
                              interval=interval, blit=True, init_func=init)

plt.show()
        
# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate() 
        
    
        
        
        
        