# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 22:38:56 2021

@author: 88698
"""



import json
import csv
from urllib.request import urlopen
import pandas as pd
import numpy as np
from tqdm import trange
from time import gmtime, strftime
from sklearn.metrics.pairwise import cosine_similarity

url = 'https://raw.githubusercontent.com/kk25gb/AIdea-project-file/main/stage2/vectorize_data.json'
response = urlopen(url)
data = json.loads(response.read())
known_assay_labels = list(data.keys())
df = pd.DataFrame(data).T

condition = df.iloc[:,:].values.sum(axis = 0) != 0
condition_d = df.values.sum(axis = 1) != 0
# df.iloc[:,condition]
ni = np.array(df.values, dtype = 'bool').sum(axis = 0)


# idf = np.log(1 + len(df.iloc[condition_d, :].index) / ni)
idf = np.log(1 + np.max(ni) / ni)
# tf = 0.5 + 0.5 * (df.values / df.values.max(axis = 1).reshape(df.values.shape[0],1))
tf = df.values 
score_df = df.copy()
score_df.iloc[:] = tf * idf

table = [['Test','Reference']]
for q in df.iloc[condition_d, :].index:
    print(q)
    condition = df.loc[q,:].values != 0
    columns= df.iloc[:,condition].columns
    class1_column = columns[columns < 369]
    class2_column = columns[np.all([columns <= 556, columns >=369], axis = 0)]
    class3_column = columns[columns >= 557]
    
    score_q = score_df.loc[q,columns].values
    # sum_q = [df.loc[q, class1_column].values.sum(), df.loc[q, class2_column].values.sum(), df.loc[q, class3_column].values.sum()]
    # print("q is {}".format(sum_q))
    
    print("q is {}".format(score_q))
    print("q is {}".format(df.loc[q, condition].values))
    
    for d in df.iloc[condition_d, :].index:
        
        if q == d:
            continue
        
        sum_d = [df.loc[d, class1_column].values.sum(), df.loc[d, class2_column].values.sum(), df.loc[d, class3_column].values.sum()]
        score_d = score_df.loc[d, columns].values
        if sum(sum_d) != 0:
            score = cosine_similarity([score_q], [score_d])      # score:0.4435233
            # score = distance.canberra([score_q], [score_d])    # score:0.0142605
            # score = distance.correlation([score_q], [score_d]) # score:0.0050659
            # score = distance.dice([score_q], [score_d])        # score:0.0142605
            if score > 0.95:
                table.append([q,d])
                print(q, "and", d, " is ", score)
                print(">>",d, "is", score_d)
                print("**",d, "is", df.loc[d, columns].values)
        
        
    # if q == "1001":
    #     break


a = df.loc[q, condition].values
b = df.loc[d, condition].values
np.corrcoef(score_q, a)

with open('./output_'+str(strftime("%Y-%m-%d %H-%M-%S", gmtime()))+'.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(table)