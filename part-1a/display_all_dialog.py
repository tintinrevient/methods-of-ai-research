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

file = open("/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/project-1/dstc2_traindev/dialogs.txt", "w")

for i in range(0, logs.__len__()):
    log = json.loads(open(logs[i]).read())
    label = json.loads(open(labels[i]).read())

    for j in range(len(log["turns"])):
        
         print("System: ", log["turns"][j]["output"]["transcript"])
         print("User: ", label["turns"][j]["transcription"])

         file.write("System: " + log["turns"][j]["output"]["transcript"])
         file.write("\n")
         file.write("User: " + label["turns"][j]["transcription"])
         file.write("\n")

    print()
    file.write("\n")
    not input("Press enter to continue")
   
file.close()
