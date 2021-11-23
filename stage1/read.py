import json

with open('vectorize_data.json',encoding='utf8') as f:
    data = json.load(f)

print(len(data['1']))