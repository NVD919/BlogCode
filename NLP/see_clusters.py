import numpy as np

clusters = np.load('clusters.npy')
sentences = open('nonzero_sentences.txt').readlines()

for cluster_num in range(15):
    print 'Cluster number '+str(cluster_num)+'\n\n\n'
    cnt = 0; 
    for cluster,sentence in zip(clusters,sentences):
        if(int(cluster)==cluster_num):
            print sentence
            cnt += 1;
        if(cnt>100):
            break;
