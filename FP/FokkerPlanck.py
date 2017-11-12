import numpy as np
import scipy as sp
from math import exp, log
from scipy.integrate import simps

N=50;            #Number of cities
gridsize = 150;  #Number of grid points to sample PDF 
h=0.75;            #Size of grid point to sample PDF
th = 0.0005;      #Size of timestep (If this is too big CFL condition will be violated)
W = 10;          #Total population (in millions)

beta = 1.;       #Multiplier for the second derivative term
xi   = 0.2;      #Multiplier for the first derivative term (equal to 2a-1) should be between -1 and +1

def A(j,P):           				#This is A(n), the Pareto function
   if j==gridsize-1:  				#The integral of one point should be 0
      return 0;
   return 1/float(N)*simps(P[j:],dx=h); 	#Use Simpson's method to do the integration

def B(j,P):					#This is B(n)
   if j==0:					#The integral of one point should be 0
      return 0;

   toIntegrate = np.zeros(j);		   	#Set up a vector to store P(n)n^2

   for k in range(j):
      toIntegrate[k] = P[k]*float(k)*float(k)*h*h/2.; 

   return 1/float(N)*simps(toIntegrate,dx=h); 	#Use Simpson's method to do the integration

def C(j,P):                                     #This is C(n)
   if j==0:
      return 0;

   toIntegrate = np.zeros(j);                   #Set up a vector to store P(n)n
   
   for k in range(j):
      toIntegrate[k] = P[k]*float(k)*h;

   return 1/float(N)*simps(toIntegrate,dx=h);   #Use Simpson's method to do the integration


def Eval(j,P):					#This is the function (n^2/2A+B)P
   return (float(j)*float(j)*h*h/2.*A(j,P)+B(j,P))*P[j];

def Eval2(j,P):					#This is the function (C+nA)P
   return (C(j,P)+float(j)*h*A(j,P))*P[j];

def Normalize(P):				#Make sure that the first moment is always N
   P /= simps(P,dx=h);
   P *= N;

def D2(j,P):			  #Use finite-differences for derivative. Forward/backward differences for the boundary
   if(j==0):
      return (Eval(j+2,P)-2.*Eval(j+1,P)+Eval(j,P))/(h*h);
   if(j==(gridsize-1)):
      return (Eval(j,P)-2.*Eval(j-1,P)+Eval(j-2,P))/(h*h);
   return (Eval(j+1,P)-2.*Eval(j,P)+Eval(j-1,P))/(h*h);


def D1(j,P):                      #Use finite-differences for derivative. Forward/backward differences for the boundary
    if(j==(gridsize-1)):
       return (Eval2(j,P)-Eval2(j-1,P))/h;
    return (Eval2(j+1,P)-Eval2(j,P))/h;


Pold = np.zeros(gridsize);	  #Store the value of P at the previous timestep
Pnew = np.zeros(gridsize);	  #Store the value of P at the current timestep

for i in range(gridsize):
   Pold[i] = float(gridsize-i)*h; #Initialize variables to exponential initially

Normalize(Pold);		  #Make sure normalization is satisfied

np.savetxt('initialvals.csv',Pold,delimiter=", ")

for i in range(5000):     	  #Step using a finite difference in time
   for j in range(gridsize):
      Pnew[j] = Pold[j] + th*beta*D2(j,Pold)-th*xi*D1(j,Pold); #Arbitrary probability of moving from one city to another 
      #Pnew[j] = Pold[j] + th*beta*D2(j,Pold)                  #Equal probability of moving from one city to another

   Pold = Pnew;		
   Normalize(Pold);               #Make sure normalization is satisfied

np.savetxt('finalvals.csv',Pold,delimiter=", ")
