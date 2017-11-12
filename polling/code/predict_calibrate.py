import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

from utils import *

dropout_frac = 0.4
model = load_model("../results/predict_results.h5",dropout_frac=dropout_frac)

percentiles = []
hundreds_count = 0
zeros_count = 0

mc_num = 1000

for in_row,out_row in file_reader('../data/val_features.csv',train=False):
    test_length = len(in_row)

    preds = []
    for i in range(mc_num):
        in_put = np.array([in_row]).astype(float)
        preds.append(model.predict(in_put)[0][0])

    percent = stats.percentileofscore(np.array(preds), float(out_row))
    percentiles.append(percent)
    if(percent==100.):
       hundreds_count +=1
    elif(percent==0.):
       zeros_count += 1

print dropout_frac
print hundreds_count
print zeros_count
print stats.kstest(percentiles, stats.uniform(loc=0.0, scale=100.0).cdf)

#Plot the results
res = stats.cumfreq(percentiles,numbins=mc_num)
plt.ylim([0.0, 1.0])
plt.xlim([0.0, 1.0])

plt.plot([1.0*x/mc_num for x in range(mc_num)],1.0*res.cumcount/len(percentiles), c='b', lw=3)
plt.plot([1.0*x/mc_num for x in range(mc_num)],[1.0*x/mc_num for x in range(mc_num)], c='g', lw=3)
plt.xlabel('Percentile')
plt.ylabel('CDF')

plt.savefig('calibration.png')





