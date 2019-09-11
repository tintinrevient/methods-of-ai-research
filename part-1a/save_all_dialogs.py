import os, json

path = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1a/dstc2_traindev/data'

logs = []
labels = []

for r, d, f in os.walk(path):
    for file in f:
        if 'log.json' in file:
            logs.append(os.path.join(r, file))
        if 'label.json' in file:
            labels.append(os.path.join(r, file))

f = open("/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1a/dialogs.txt","w+")

for i in range(logs.__len__()):
    log = json.loads(open(logs[i]).read())
    label = json.loads(open(labels[i]).read())

    for j in range(len(log["turns"])):
         f.write("System: " + log["turns"][j]["output"]["transcript"] + "\n")
         f.write("User: " + label["turns"][j]["transcription"] + "\n")

    f.write("\n")

f.close()
