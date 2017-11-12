import numpy as np
import pandas as pd
import glob
from sklearn.decomposition import ProjectedGradientNMF

dontuse = ['SID','Name','Grader','Comments','Submission Time','Lateness','Question ID','Adjustment','Score'];  	#These are either irrelevant or hard to include in the analysis

path ='/Phys_7B_-_Lecture_2_Midterm_1'                                                                         	#Directory with the Gradescope files
offset = 0;                                                                                                    	#Makes sure files read correctly
allFiles = glob.glob(path + "/*.csv")

d = {'true':1.0,'false':0.0};                                                                                  	#Dictionaries to replace booleans with numbers
notd = {'true':0.0,'false':1.0};

init = False;                                                                                                  	#Track if this is the first iteration
ptvals = {};                                                                                                  	#Stores point values of rubric items

for files in allFiles:                                                                                         	#Loop over all problems
    pth = files[files.rfind('/')+1:];                                                                          	#Get the filename to track problem
    if ("scores" in files):                                                                                    	#The score file just gives us total score and emails
       df = pd.read_csv(files,usecols=['Email','Total Score']);
    else:
       df = pd.read_csv(files);
       df = df.fillna(0);
       tal = df.tail(3);                                                                                       	#The last three lines have point information
       df = df.drop(tal.index);
       tal = np.array(tal);

       if(tal[2,1] == "negative"):
          sgn = -1.;
       else:
          sgn = 1.;
       
       usecols = ["Email"];											#Track which columns have useful information

       for i in range(5-offset,len(df.columns)-offset):								
          if(df.columns[i+offset] not in dontuse):
             pntval = float(tal[0,i])*sgn;
             if(pntval>0):											#If positive points, use column, use positive dictionary
                col = df.columns[i+offset]+" "+pth;
                used = d;
             elif(pntval<0):											#If negative points, use complement of column, use negative dictionary
                col = "NOT "+df.columns[i+offset]+" "+pth;
                pntval *= -1;
                used = notd;

             while(col in ptvals):										#If grader gave a duplicate name to a rubric item, attach "A" to make it no longer duplicate
                col += "A";

             usecols.append(col);										#Attach this new columns to the columns being used
             df = df.rename(columns = {df.columns[i+offset]:col});                                              #Rename the column in df
             df[col] = df[col].replace(used)*pntval;                                                            #Convert from boolean to points
             ptvals[col] = pntval;                                                                              #Store point values for rubric item
             
       df = df[usecols];                                                                                      	#Only keep relevant columns


    if(init):
          frame = pd.merge(frame,df,on='Email',how='left',suffixes=['',str(files)])				#If not first time, merge on emails
    else:
       frame = df;												#If first time, make the master dataframe
       init = True;

frame = frame.sort('Total Score',ascending = False);								#Sorting by Overall Score is interesting
fr = frame.drop('Email',1);											#NMF will not use email or total score
fr = fr.drop('Total Score',1);

feature_names = fr.columns;

X = np.array(fr.astype(float));

'''for i in range(60):												#Test error as a function of number of topics

   model = ProjectedGradientNMF(n_components=i, init='nndsvda',random_state=0,max_iter=500)
   model.fit(X)

   print (i,model.reconstruction_err_);'''

model = ProjectedGradientNMF(n_components=11, init='nndsvda',random_state=0,max_iter=500)                       #Perform the NMF
Xtrans = model.fit_transform(X)

for topic_idx, topic in enumerate(model.components_):								#Print the rubric items with strongest contribution in topics 
    sorte = np.sort(topic)[::-1];
    sorteargs = np.argsort(topic)[::-1];
    i = 0;
    print("Topic #%d:" % topic_idx)
    while(sorte[i]>1.5):                                                                                        #Only show things where contribution is large (1.5 is arbitrary)
       print feature_names[sorteargs[i]],np.mean(np.transpose(X)[sorteargs[i]])/ptvals[feature_names[sorteargs[i]]];
       i += 1;
    sm = 0.;
    nrm = 0.;
    for k in range(len(topic)):										 	#Find how many points are associated with the topic
       sm += topic[k]*ptvals[feature_names[k]];
       nrm += topic[k];
    print sm/nrm;

    print("\n");
