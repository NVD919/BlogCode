import numpy as np
import pandas as pd
import math
from datetime import datetime
from sklearn.ensemble import GradientBoostingRegressor

df = pd.read_csv('DNCArrivalData.csv',sep="\t",header=None)

df = df[(df[0]==79)&(df[3]>-1)]

df[1] = (pd.to_datetime(df[1].str[:10])-pd.to_datetime("07/04/2006")).astype(np.int64)/86400000000000;
df[3] = (pd.to_datetime(df[3])-pd.to_datetime("5:24PM")).astype(np.int64)/60000000000;

usevars = [1,3];

df = df[usevars]

test = df[df[1]>3145]
test = np.sort(np.array(test[3]));

print test;

interval = [183,365,548,730,913,1095,1278,1460,1643,1825];

testper = [0.3,0.6827,0.8,0.9,0.95,0.99];

for end in interval:
   print end
   train = df[(df[1]<3146)& (df[1]>3146-end)];
   train = np.sort(np.array(train[3]));

   for per in testper:
      v = train[np.floor(len(train)*(1-per))];
      for q in range(len(test)):
         if test[q]>v:
            print float(q)/len(test);
            break;
