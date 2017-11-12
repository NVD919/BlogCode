import numpy
from math import exp

size = 250;                   #Squareroot of total number of voters
T = 2.;                       #Temperature of the system. I assume epsilon=1
beta = 0.3;                   #This is actually beta/T

s = numpy.zeros((size,size)); #Stores voter's vote. Could be an bitwise integer to save space
h = numpy.zeros((size,size)); #Sotres h values for each voter

for i in range(size):
   for j in range(size):
      s[i,j] = numpy.random.choice((-1.,1.));        #Initialize each voter randomly

for i in range(size):                                #Assign h values in preferred way
   for j in range(size):
      #h[i,j] = numpy.random.uniform(-beta,beta);
      if( i < size/2.1):
         h[i,j] = numpy.random.uniform(-beta,0);
      else:
         h[i,j] = numpy.random.uniform(0,beta);  
      #h[i,j] = (2.*float(j)/float(size)-1.)*beta;

for k in range(10000000):
   i = numpy.random.choice(size);                    #Choose a random voter
   j = numpy.random.choice(size);

   if(i == 0):                                       #Get information about the neighbors
      top = s[size-1,j];
   else: 
      top = s[i-1,j];

   if(j == 0):
      left = s[i,j-1];
   else:
      left = s[i,j-1];

   if( i == size-1):
      bottom = s[0,j];
   else:
      bottom = s[i+1,j];

   if( j== size-1):
      right = s[i,0];
   else:
      right = s[i,j+1];
   
   Delta = 2.*s[i,j]*(top+bottom+left+right)+beta*s[i,j]*h[i,j]; #This is the energy change if the voter changes vote

   if(Delta <= 0.):                                  #Always accept if it decreases energy
      s[i,j] *= -1.;
   else:
      if(numpy.random.uniform() < exp(-Delta/T)):    #Conditionally accept relative to Boltzmann factor if it increases energy
         s[i,j] *= -1.;

totsum = 0;

for i in range(size):
   for j in range(size):
      totsum += s[i,j]                               #See which candidate won

print totsum;

numpy.savetxt('finalstate.csv',s, delimiter=", ")    #Store the output
