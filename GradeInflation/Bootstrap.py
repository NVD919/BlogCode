import random;
import numpy as np;
import matplotlib.pyplot as plt

numstudents = 350;
classsizes = [100,250,350]; #Cumulative number of students in each class
classes = [[],[],[]];       #Will store arrays of students in each class
student = [];               #Will store rank of each student in each bootstrapped class
xs = [];                    #Will store "true" rank of each student
truepercentile = [];        #Will store "true" percentile of each student

for i in range(numstudents):  #Initiate arrays
    student.append([]);
    xs.append(i);
    truepercentile.append(1.-float(i)/numstudents);

for k in range(10000):      #Bootstrap array
   perm = np.random.permutation(numstudents); #Take a random permutation of students as a class assignment
   
   classes[0] = sorted(perm[:classsizes[0]]); #Rank the students in each class
   classes[1] = sorted(perm[classsizes[0]:classsizes[1]]);
   classes[2] = sorted(perm[classsizes[1]:]);
   

   for j in range(3):      #Update the student array with the student's percentile in this particular instance
      i = 0.;
      for x in classes[j]:
         student[x].append(1-i/len(classes[j]));
         i += 1;

lowerlims = [];            #Store 90% confidence region on percentile as well as grade ranges
upperlims = [];
Top = [];
As = [];
Ams = [];
Bps = [];
Bs = [];
Bms = [];
Cps = [];
Cs = [];
Cms = [];
Ds = [];

for arr in student:
   arr = sorted(arr);
   lowerlims.append(arr[10000/20]);
   upperlims.append(arr[10000-10000/20]);
   Top.append(1.0);
   As.append(0.875);
   Ams.append(0.75);

   Bps.append(0.617);
   Bs.append(0.483);
   Bms.append(0.35);

   Cps.append(0.25);
   Cs.append(0.15);
   Cms.append(0.05);

   Ds.append(0.);


#Do the plotting
plt.plot(xs,lowerlims,color="black")
plt.xlabel("True Rank",fontsize=18);
plt.ylabel("Class Percentile",fontsize=18);
plt.plot(xs,upperlims,color="black")
plt.plot(xs,truepercentile,color="black")
plt.fill_between(xs,As,Top,color="purple",alpha=0.2);
plt.text(8, .88, 'A',fontsize=14)
plt.text(8, .76, 'A-',fontsize=14)
plt.text(8, .63, 'B+',fontsize=14)
plt.text(8, .49, 'B',fontsize=14)
plt.text(8, .36, 'B-',fontsize=14)
plt.text(8, .26, 'C+',fontsize=14)
plt.text(8, .16, 'C',fontsize=14)
plt.text(8, .06, 'C-',fontsize=14)
plt.text(8, .005, 'D',fontsize=14)
plt.fill_between(xs,Ams,As,color="cyan",alpha=0.2);
plt.fill_between(xs,Bps,Ams,color="blue",alpha=0.2);
plt.fill_between(xs,Bs,Bps,color="green",alpha=0.2);
plt.fill_between(xs,Bs,Bms,color="yellow",alpha=0.2);
plt.fill_between(xs,Bms,Cps,color="orange",alpha=0.2);
plt.fill_between(xs,Cps,Cs,color="darksalmon",alpha=0.2);
plt.fill_between(xs,Cs,Cms,color="brown",alpha=0.2);
plt.fill_between(xs,Cms,Ds,color="red",alpha=0.2);

plt.axis([0.0,float(numstudents), 0.0,1.0])
plt.savefig("fluctuation.png");
