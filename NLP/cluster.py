import numpy as np
from sklearn.cluster import MiniBatchKMeans

db = MiniBatchKMeans(n_clusters = 50,batch_size=20000,verbose=True)
X = np.load('all_sentence_vecs.npy')
db.fit(X)

labels = db.labels_
np.save('clusters', labels)
