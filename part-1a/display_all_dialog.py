import os, json

path = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/project-1/dstc2_traindev/data'

logs = []
labels = []

for r, d, f in os.walk(path):
    for file in f:
        if 'log.json' in file:
            logs.append(os.path.join(r, file))
        if 'label.json' in file:
            labels.append(os.path.join(r, file))

for i in range(0, logs.__len__()):
    log = json.loads(open(logs[i]).read())
    print("system: ", log["turns"])
    label = json.loads(open(labels[i]).read())
    print("user: ", label["turns"])


