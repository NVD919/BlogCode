import numpy

def main(alf,bet): #Arguments are value of alpha/temperature and value of beta/temperature

    N = 65; #Total capacity of the bus
    n = 35; #Number of people to get on the bus
    eps = numpy.zeros(N); #Array of seat energies divided be temperature, default is standing in front which is 0
    seated = numpy.zeros(N); #Array will keep track of which positions are taken

    for i in range(0,15):
       eps[i] = -alf; #Set values for seats in front

    for i in range(15,35):
       eps[i] = -alf+bet; #Set values for seats in back

    for i in range(35,51):
       eps[i] = bet; #Set values for standing in back


    mu = FindMu(eps,n); #Get the chemical potential for the system
    tot = n; #The total current occupancy is all the people to get on the bus

    frontseatcount = 0;
    backseatcount = 0;
    backstandcount = 0;
    standcount = 0;

    for i in range(0,n):
       rand = numpy.random.uniform(0.,tot); #Determine an occupancy value that will be filled
       test = 0.;
       j = 0;
       while(test<rand):
          if(seated[j]==0.0):
             test += 1./(numpy.exp(eps[j]-mu)+1.); #Add up occupancies until values is greater than rand, and take that seat
          
          j += 1;

       seated[j-1] = 1.;

       #Collect data on which type of seats are filled
       if(j-1<15):
          frontseatcount += 1;
       elif(j-1<35):
          backseatcount += 1;
       elif(j-1<51):
          backstandcount += 1;
       else:
          standcount += 1;

       tot -= 1./(numpy.exp(eps[j-1]-mu)+1.); #Subtract off occupancy from the occupied seat

    print "Output is number of occupied seats for (front sitting, back sitting, front standing, back standing)"
    print (frontseatcount,backseatcount,standcount,backstandcount);


def FindMu(eps,n): #Use secant method to find mu where the sum of all occupancies is n
   B0 = -10.;
   B1 = 0.;

   val0 = n-GetTotOccup(eps,B0);
   val1 = n-GetTotOccup(eps,B1);
   update = 1;

   while(numpy.abs(val0)>1e-5):
      update = val1*(B1-B0)/(val1-val0);
      B0 = B1;
      B1 -= update;
      val0 = val1;
      val1 = n-GetTotOccup(eps,B1);

   return (B0+B1)/2.;


def GetTotOccup(eps,mu): #Sums up the occupancy over all the energy states
   tot = 0.;
   for ener in eps:
      tot += 1./(numpy.exp(ener-mu)+1.);

   return tot;
