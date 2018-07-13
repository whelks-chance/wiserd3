import json

with open('data.json', 'r+') as f:
    data = json.load(f)
# for element in data:
#     del element['']
print data
