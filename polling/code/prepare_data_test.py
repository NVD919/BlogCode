import pandas as pd
import numpy as np
from scipy import stats

df_prev = pd.read_csv('../data/raw-polls.csv')
df_prev['poll_datetime'] = pd.to_datetime(df_prev['polldate'])

df = pd.read_csv('../data/president_general_polls_2016.csv')
df['poll_datetime'] = pd.to_datetime(df['enddate'])
df['election_datetime'] = pd.to_datetime('2016/11/08')
df['days_to_election'] = 1.0*(df['election_datetime'] - df['poll_datetime']).dt.days/365

df = df[(df['days_to_election']<=21./365) & (df['type']=='polls-plus')]

party_dict = {'R': -1., 'D': 1., '': 0., 'I': 0.}

df_summary = pd.read_csv('../data/pollster-ratings-partisan.csv')
df_summary.index = df_summary['Pollster']
yes_dict = {'yes': 1., 'no': 0.}
df_summary['Live Caller With Cellphones'] = df_summary['Live Caller With Cellphones'].apply(lambda x: yes_dict[x])
df_summary['Internet'] = df_summary['Internet'].apply(lambda x: yes_dict[x])
df_summary['NCPP/AAPOR/Roper'] = df_summary['NCPP/AAPOR/Roper'].apply(lambda x: yes_dict[x])

df_groups = df.fillna(0).groupby('state')

test_file = open('../data/test_features.csv','wb')

for name,group in df_groups:
    poll_times = np.array(group.days_to_election.tolist())
    sort_index = np.argsort(poll_times)[::-1]
    poll_times = poll_times[sort_index]

    poll_date = np.array(group.poll_datetime.tolist())[sort_index]
    pollster_list = np.array(group.pollster.tolist())[sort_index]

    cand1_pct = np.array(group.rawpoll_clinton.tolist())[sort_index]/100.0
    cand2_pct = np.array(group.rawpoll_trump.tolist())[sort_index]/100.0
    cand3_pct = np.array(group.rawpoll_johnson.tolist())[sort_index]/100.0
    sample_size = np.array(group.samplesize.tolist())[sort_index]

    if(True):
        input_features = []
        output = []

        for t,pct1,pct2,pct3,siz,pollster_name,date in zip(poll_times,cand1_pct,cand2_pct,cand3_pct,sample_size,pollster_list,poll_date):
            pollster_counts = df_prev[df_prev['poll_datetime'] <= date].groupby('pollster').apply(lambda x: len(x))

            if pollster_name in df_summary.index:
                live_caller = df_summary.loc[pollster_name]['Live Caller With Cellphones']
                internet = df_summary.loc[pollster_name]['Internet']
                member = df_summary.loc[pollster_name]['NCPP/AAPOR/Roper']
                partisan = party_dict[df_summary['Partisan'].fillna('I').loc[pollster_name]]
                partisan_known = df_summary['Partisan'].isnull().astype(float).loc[pollster_name]
                pollster_pctile = stats.percentileofscore(pollster_counts.tolist(),pollster_counts.loc[pollster_name])/100.0

            else:
                live_caller = 0.
                internet = 0.
                member = 0.
                partisan = 0.
                partisan_known = 1.0
                pollster_pctile = 0
                 
                print pollster_name

            input_features.append([t,pct1,pct2,pct3,np.tanh(float(siz)/1000),partisan,partisan_known,live_caller,internet,member,pollster_pctile])
            test_file.write(str(input_features)+",'"+name+"'\n")

test_file.close()

