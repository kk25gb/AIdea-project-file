import json

results={}

with open('./chem_list.json',encoding='utf8') as f:
    chem_list = json.load(f)

with open('./crop_list.json',encoding='utf8') as f:
    crop_list = json.load(f)

with open('./pest_list.json',encoding='utf8') as f:
    pest_list = json.load(f)

index_list = {**chem_list,**crop_list}
index_list = {**index_list,**pest_list}

def find_index(input):
    results=[]
    keys = list(input.keys())
    for key , value in input.items():
        results.append([key,keys.index(key)])
        if len(value)>0:
            for char in value:
                results.append([char,keys.index(key)])

    return results

index_list = find_index(index_list)


for row in index_list:
    results[row[0]] = row[1]

with open('./index_dict.json', 'w', encoding='utf8') as f:
    json.dump(results, f, ensure_ascii=False)
