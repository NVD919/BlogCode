from gensim.models import Word2Vec
import numpy as np
from utils import MySentences
from sklearn.decomposition import PCA

model = Word2Vec.load('twitch_corpus.wv')

pca = IncrementalPCA(n_components=2)
total_counts = 1000000
sentences = MySentences('random_lines.txt',randomize=False)

full_matrix = np.zeros((total_counts,200)).astype(float)

nonzero_file = open("nonzero_sentences.txt","w") 
tot_cnt = 0;

for line in sentences:
    sentencevec = np.zeros(200).astype(float)
    cnt=0

    for word in line:
        if word in model.wv.vocab:
            sentencevec += model.wv.word_vec(word,use_norm=True)
            cnt += 1;

    if(cnt>0):    
        full_matrix[tot_cnt,:] = sentencevec/cnt
        tot_cnt += 1
        nonzero_file.write(str(line)+'\n')

    if(tot_cnt>=total_counts):
        break;

pca = PCA(n_components=2)
pca.fit_transform(full_matrix)

nonzero_file.close();
np.save('all_sentence_vecs',full_matrix)
np.save('pca_all_sentence_vecs',pca.transform(full_matrix))

