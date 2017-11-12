import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils import *

dropout_frac = 0.4
mc_num = 1000

model = load_model("../results/predict_results_all.h5",dropout_frac=dropout_frac)
win_probs = []

for day in range(14)[::-1]:
    tot_evs = np.zeros((mc_num,1))
    for state in ev_dict.keys():
        use_input = [];
        for in_row,in_state in file_reader('../data/test_features.csv',train=False):
            if((state==in_state) and (in_row[-1][0]*365.>=day) and (len(in_row)>len(use_input))):
                use_input = in_row

        for i in range(mc_num):
            in_put = np.array([use_input]).astype(float)
            if(model.predict(in_put)[0][0] > 0):
                tot_evs[i] += ev_dict[state]

    win_probs.append([day,100.0*len([x for x in tot_evs if x>=270])/mc_num])

    plt.hist(tot_evs, 50, facecolor='g', alpha=0.3,density=1)
    plt.axvline(x=270, color='r', linestyle='-')
    plt.xlabel('Electoral Votes Won by Democrat')
    plt.xlim([0,538])

    plt.savefig('hist_{}.png'.format(day))
    plt.clf()

plt.plot(np.array(win_probs)[:,0],np.array(win_probs)[:,1], c='b', lw=3)
plt.xlabel('Days until election')
plt.ylabel('Probability of Democratic Victory')
plt.gca().invert_xaxis()

plt.savefig('win_prob.png')








