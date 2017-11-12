import numpy as np
import scipy as sp
from math import sin,cos,sqrt,exp

vd = 1.4;     #in m/s
tau = 0.33;   #in s
dt = 0.1;     #is s, reduce for more accuracy

ymax = 5.;    #in m, width of the corridor
xmax = 50.;   #in m, length of the corridor

gamma = 0.5;  #Strength of interaction force
eps = 0.1;    #Regulator for interaction force
r0 = 1.2;     #in m, range of interaction force

A = 5.;       #Strength of wall force, Choose to be approximately vd/tau
lb = ymax/20; #range of influence of the wall

p = 0.9;      #Proportion of left-goers to right goers

class Ped:

   def __init__(self):                                        #This is called when particle is initialized
      self.x = [xmax*np.random.rand(),ymax*np.random.rand()]; #Randomly place pedestrian in room
      theta = 2.*np.pi*np.random.rand();                      #Choose a random direction for the pedestrian's velocity

      self.v = [vd*sin(theta),vd*cos(theta)];                 #Magnitude of velocity is vd
      self.a = [0.,0.];                                       #No acceleration initially
      self.t0 = 0.;                                           #Will keep track of when the pedestrian enters room

      if(np.random.rand()>p):                                 #Choose a random direction that the pedestrains desire to go
         self.dir = 1.;
      else:
         self.dir = -1.;

   def euler(self,t):                                         #Implicit Euler method to move the pedestrians a timestep dt
      toReturn = 0.;                                          #This will store how much time it took for the pedestrian to cross the room

      self.v[0] += self.a[0]*dt;                              #This is the Euler method, update velocity first
      self.v[1] += self.a[1]*dt;

      self.a[0] = 0.;                                         #Set the forces on the particle to zero again
      self.a[1] = 0.;

      self.x[0] += self.v[0]*dt;                              #Now update the position
      self.x[1] += self.v[1]*dt;

      if( (self.dir > 0) & (self.x[0] > xmax)):               #If particle is at the end of the room
          if(self.t0>0.):                                     #Make sure the particle started at the other end of the room
             toReturn = t-self.t0;                            #How much time it took to cross the room
          self.restart(t);

      elif( (self.dir < 0) & (self.x[0] < 0)):
          if(self.t0>0.):
             toReturn = t-self.t0;
          self.restart(t);

      return toReturn;

   def restart(self,t):                                       #Randomly generate a particle at the other end
      if self.dir >0:
         self.x = [0., ymax*np.random.rand()];                #Assign a random y position, and a random direction toward the goal end
         theta = (np.pi*np.random.rand())-np.pi/2.;

      else:
         self.x = [xmax, ymax*np.random.rand()];            
         theta = (np.pi*np.random.rand())+np.pi/2.;

      self.v = [vd*sin(theta),vd*cos(theta)];
      self.t0 = t;

def Nbody(N):
   peds = [];                 #Stores all the pedestrians

   for i in range(N):         #Make N pedestrians
      peds.append(Ped());

   t=0.;

   dev = open("data.txt", "wt");    #These data files with store positions of pedestrians and the time it takes to cross the room
   dev2 = open("times1.txt","wt");
   dev3 = open("times2.txt","wt");
   while(int(t/dt)<5000):           #We will simulate 5000 time steps
      for i in range(N):
         peds[i].a[0] += (vd*peds[i].dir-peds[i].v[0])/tau; #This is the restorative force
         peds[i].a[1] += -peds[i].v[1]/tau;         

         peds[i].a[1] += A*(exp(-peds[i].x[1]/lb)-exp(-(ymax-peds[i].x[1])/lb)) #This is the wall force
         
         if int(t/dt)%2 == 0:
            print >> dev, peds[i].x[0], peds[i].x[1], int(peds[i].dir+2) #Store the position of the pedestrians

         for j in range(i+1,N):   #This is the generalized Coulomb force, calculate between all pedestrians
            dx = peds[i].x[0]-peds[j].x[0];
            dy = peds[i].x[1]-peds[j].x[1];
            dij = sqrt(dx*dx+dy*dy);
            fpart = gamma/(pow(dij/r0,3)+eps);

            peds[i].a[0] += dx*fpart;
            peds[i].a[1] += dy*fpart;

            peds[j].a[0] -= dx*fpart;
            peds[j].a[1] -= dy*fpart;

         time = peds[i].euler(t); #Step the particle a time step dt
         if(time>0.):
            if(peds[i].dir<0):    #If pedestrian made it to the end, store the data
               print >> dev2, time
            else:
               print >> dev3, time

      if int(t/dt)%2 == 0:        #Put some whitespace in the data file so gnuplot will like it
         print >> dev
         print >> dev

      t += dt;                    #We change the time by dt

   dev.close()
   dev2.close()
   dev3.close()
