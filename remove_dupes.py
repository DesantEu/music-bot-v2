import json

rJson = {}
with open("saves/cache.json", "r") as file:
    rJson = json.loads(file.read())
    
    for i in rJson:
        i['searches'] = list(set(i['searches']))

with open("saves/cache.json", "w") as file:
    file.write(json.dumps(rJson))


