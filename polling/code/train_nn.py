import numpy as np
import pandas as pd
from keras.optimizers import Adam

from utils import *

def fit_generator(dat_file,batch_size,max_seq_len = 1000,seq_elem_len = 11):
    X = np.zeros((batch_size,max_seq_len,seq_elem_len))
    Y = np.zeros(batch_size)

    while True:
        total_cnt = 0
        batch_cnt = 0

        max_len = 1;
        for in_row,out_row in file_reader(dat_file):
            test_length = len(in_row)

            if(test_length>max_len):
                max_len = test_length   

            X[batch_cnt,-test_length:,:] = np.array(in_row).astype(float)
            Y[batch_cnt] = float(out_row)
            batch_cnt += 1

            if batch_cnt >= batch_size:
                yield X[:,-max_len:,:], Y

                X[:] = 0.
                Y[:] = 0.
                total_cnt += batch_cnt
                batch_cnt = 0
                max_len = 1 
  
        if batch_cnt > 0:
            yield X[:batch_cnt,-max_len:,:],Y[:batch_cnt]
            total_cnt += batch_cnt

model = load_model('')
adam = Adam(lr=0.0001)
model.compile(loss='mean_squared_error', optimizer=adam,metrics = ['accuracy'])
model.summary()

minibatch_size = 32

samples_per_epoch = 6213
steps_per_epoch =int(np.ceil(samples_per_epoch * 1.0 / minibatch_size))

epoch_sizes = []
fg = fit_generator('../data/train_and_val_features.csv',minibatch_size)

model.fit_generator(generator=fg,
                        steps_per_epoch=steps_per_epoch,
                        epochs=10)

model.save("../results/predict_results_all.h5")
