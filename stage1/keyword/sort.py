import os
import json

results = {}
file_list = [name.replace('.txt','') for name in os.listdir('./dataTrainComplete')]
del file_list[file_list.index('887')] # delete the problem assay
print(file_list)

for i in file_list:
    contnet = open('./dataTrainComplete/'+i+'.txt', 'r', encoding='utf-8',errors='ignore').read()
    # print()
    results[i]=contnet.replace('\n','')
    # break
with open('../../assays.json', 'w', encoding='utf8') as f:
    json.dump(results, f, ensure_ascii=False)