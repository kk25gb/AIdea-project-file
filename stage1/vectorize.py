import json
import re

results = {}

with open('dataTrainComplete.json',encoding='utf8') as f:
    data = json.load(f)

with open('./keyword/chem_list.json',encoding='utf8') as f:
    chem_list = json.load(f)

with open('./keyword/crop_list.json',encoding='utf8') as f:
    crop_list = json.load(f)

with open('./keyword/pest_list.json',encoding='utf8') as f:
    pest_list = json.load(f)


def find_pattern(input,list):
    results=[]
    for key , value in list.items():
        num = len(re.findall(key,input))
        if len(value)>0:
            for char in value:
                num += len(re.findall(char,input))
        results.append(num)

    return results


for key , value in data.items():
    temp = {}
    # print(value)
    temp['chem']=find_pattern(value,chem_list)
    temp['crop']=find_pattern(value,crop_list)
    temp['pest']=find_pattern(value,pest_list)
    results[key]=temp

with open('./vectorize_data.json', 'w', encoding='utf8') as f:
    json.dump(results, f, ensure_ascii=False)
