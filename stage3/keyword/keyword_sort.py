# import os
import pandas as pd
import json

def sort_function(input):
    results = {}
    for index, row in input.iterrows():
        temp = [x for x in list(row) if x == x]
        results[temp[0]]=temp[1:]
    return results


chem_list = sort_function(pd.read_excel('./02chem.list.xlsx',header=None))
crop_list = sort_function(pd.read_excel('./02crop.list.xlsx',header=None))
pest_list = sort_function(pd.read_excel('./02pest.list.xlsx',header=None))

# print(chem_list)
# print(crop_list)
# print(pest_list)

with open('../../chem_list.json', 'w', encoding='utf8') as f:
    json.dump(chem_list, f, ensure_ascii=False)

with open('../../crop_list.json', 'w', encoding='utf8') as f:
    json.dump(crop_list, f, ensure_ascii=False)

with open('../../pest_list.json', 'w', encoding='utf8') as f:
    json.dump(pest_list, f, ensure_ascii=False)