from keras import backend as K

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Masking
from keras.layers import LSTM
from keras.layers import Lambda

import random
import ast

#Dictionary of electoral votes
ev_dict = {'Alabama':9,
           'Montana':3,
           'Alaska':3,
           'Nebraska':5,
           'Arizona':11,
           'Nevada':6,
           'Arkansas':6,
           'New Hampshire':4,
           'California':55,
           'New Jersey':14,
           'Colorado':9,
           'New Mexico':5,
           'Connecticut':7,
           'New York':29,
           'Delaware':3,
           'North Carolina':15,
           'Florida':29,
           'North Dakota':3,
           'Georgia':16,
           'Ohio':18,
           'Hawaii':4,
           'Oklahoma':7,
           'Idaho':4,
           'Oregon':7,
           'Illinois':20,
           'Pennsylvania':20,
           'Indiana':11,
           'Rhode Island':4,
           'Iowa':6,
           'South Carolina':9,
           'Kansas':6,
           'South Dakota':3,
           'Kentucky':8,
           'Tennessee':11,
           'Louisiana':8,
           'Texas':38,
           'Maine':4,
           'Utah':6,
           'Maryland':10,
           'Vermont':3,
           'Massachusetts':11,
           'Virginia':13,
           'Michigan':16,
           'Washington':12,
           'Minnesota':10,
           'West Virginia':5,
           'Mississippi':6,
           'Wisconsin':10,
           'Missouri':10,
           'Wyoming':3,
           'District of Columbia':3}

state_abbrev = {'AK': 'Alaska',
                'AL': 'Alabama',
                'AR': 'Arkansas',
                'AS': 'American Samoa',
                'AZ': 'Arizona',
                'CA': 'California',
                'CO': 'Colorado',
                'CT': 'Connecticut',
                'DC': 'District of Columbia',
                'DE': 'Delaware',
                'FL': 'Florida',
                'GA': 'Georgia',
                'GU': 'Guam',
                'HI': 'Hawaii',
                'IA': 'Iowa',
                'ID': 'Idaho',
                'IL': 'Illinois',
                'IN': 'Indiana',
                'KS': 'Kansas',
                'KY': 'Kentucky',
                'LA': 'Louisiana',
                'MA': 'Massachusetts',
                'MD': 'Maryland',
                'ME': 'Maine',
                'MI': 'Michigan',
                'MN': 'Minnesota',
                'MO': 'Missouri',
                'MP': 'Northern Mariana Islands',
                'MS': 'Mississippi',
                'MT': 'Montana',
                'NA': 'National',
                'NC': 'North Carolina',
                'ND': 'North Dakota',
                'NE': 'Nebraska',
                'NH': 'New Hampshire',
                'NJ': 'New Jersey',
                'NM': 'New Mexico',
                'NV': 'Nevada',
                'NY': 'New York',
                'OH': 'Ohio',
                'OK': 'Oklahoma',
                'OR': 'Oregon',
                'PA': 'Pennsylvania',
                'PR': 'Puerto Rico',
                'RI': 'Rhode Island',
                'SC': 'South Carolina',
                'SD': 'South Dakota',
                'TN': 'Tennessee',
                'TX': 'Texas',
                'UT': 'Utah',
                'VA': 'Virginia',
                'VI': 'Virgin Islands',
                'VT': 'Vermont',
                'WA': 'Washington',
                'WI': 'Wisconsin',
                'WV': 'West Virginia',
                'WY': 'Wyoming'}

def file_reader(file_name,train=True):
    f_buff = open(file_name).readlines()
    if(train):
        random.shuffle(f_buff)

    for row in f_buff:
        x, out = ast.literal_eval(row)
        yield x,out

#Model architecture used
def load_model(model_name,dropout_frac=0.4):
    model = Sequential() 
    model.add(Masking(mask_value=0.0,input_shape=(None,11),name='mask_0'))
    model.add(LSTM(256,return_sequences=True,name='lstm_0'))
    #Use Lambda layers so dropout at prediction time is available
    model.add(Lambda(lambda x: K.dropout(x, level=dropout_frac),name='dropout_0'))
    model.add(LSTM(256,return_sequences=True,name='lstm_1'))
    model.add(Lambda(lambda x: K.dropout(x, level=dropout_frac),name='dropout_1'))
    model.add(LSTM(256,name='lstm_2'))
    model.add(Lambda(lambda x: K.dropout(x, level=dropout_frac),name='dropout_2'))
    model.add(Dense(512,activation='relu',name='dense_0'))
    model.add(Lambda(lambda x: K.dropout(x, level=dropout_frac),name='dropout_3'))
    model.add(Dense(512,activation='relu',name='dense_1'))
    model.add(Lambda(lambda x: K.dropout(x, level=dropout_frac),name='dropout_4'))
    model.add(Dense(1,activation='linear',name='dense_2'))
    if(model_name):
        model.load_weights(model_name,by_name=True)
    return model

def load_state_model(model_name,dropout_frac=0.1):
    model = Sequential() 
    model.add(Dense(128,activation='relu',input_shape=(52,),name='dense_0'))
    model.add(Lambda(lambda x: K.dropout(x, level=dropout_frac),name='dropout_1'))
    model.add(Dense(128,activation='relu',name='dense_1'))
    model.add(Lambda(lambda x: K.dropout(x, level=dropout_frac),name='dropout_2'))
    model.add(Dense(51,activation='linear',name='dense_2'))
    if(model_name):
        model.load_weights(model_name,by_name=True)
    return model
