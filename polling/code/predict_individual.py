import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

from utils import *

mc_num = 1000
model = load_model('../results/predict_results_all.h5')

bottom_preds = []
top_preds = []

for in_row in file_reader('../data/pennsylvania_features.csv',train=False):

    preds = []
    for i in range(mc_num):
        in_put = np.array([in_row]).astype(float)
        preds.append(model.predict(in_put)[0][0])

    poll_date = in_row[-1][0]*365.

    #Get 90% confidence interval centered at the median
    bottom = 100.0*np.percentile(preds,5.)
    top = 100.0*np.percentile(preds,95.)

    if len(bottom_preds)>0:
        if(bottom_preds[-1][0] != poll_date):
            bottom_preds.append([poll_date,bottom])
            top_preds.append([poll_date,top])
        else:
            bottom_preds[-1][:] = [poll_date,bottom]
            top_preds[-1][:] = [poll_date,top]
    else:
        bottom_preds.append([poll_date,bottom])
        top_preds.append([poll_date,top])

bottom_preds = np.array(bottom_preds)
top_preds = np.array(top_preds)

plt.fill_between(bottom_preds[:,0], bottom_preds[:,1], top_preds[:,1], facecolor='green', interpolate=True,alpha=0.3)
plt.axhline(y=-0.72, color='r', linestyle='-')
plt.gca().invert_xaxis()
plt.xlabel('Days until election')
plt.ylabel('Margin')

plt.savefig('../results/pennsylvania_predictions.png')






