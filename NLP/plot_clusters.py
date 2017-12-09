import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

sentence_vecs = np.load('pca_all_sentence_vecs.npy')
color_list = np.load('clusters.npy')

color_dict = {0:'tomato',1:'black',2:'lightsalmon',3:'cyan',
              4:'lightsalmon',5:'fuchsia',6:'tomato',
              7:'yellow',8:'black',9:'black',10:'limegreen',
              11:'fuchsia',12:'cyan',13:'black',14:'lightsalmon'}
color_vecs = np.vectorize(color_dict.get)(color_list)

fig, ax = plt.subplots()

plt.scatter(sentence_vecs[:,0],sentence_vecs[:,1],s=0.5,alpha=0.1,c=color_vecs)
plt.axis('off')

ax.set_xlim(-0.4,0.4)
ax.set_ylim(-0.3,0.4)
plt.savefig('out_sentence_zoom_test_pca_all.png',dpi=1000)
plt.close()
