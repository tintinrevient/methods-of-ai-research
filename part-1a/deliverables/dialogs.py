import os, json

# Read the source data and display the dialogs one by one in human-readable format.
# Use the Enter key to proceed to the next dialog.
# Use <KeyboardInterrupt> (Ctr+C) to escape
# Input: 
# path: <str> the relative path of the input root directory 'dstc2_traindev/data/'
def displayAllDialogs(path):
    logs = []
    labels = []
    for r, d, f in os.walk(path):
        for file in f:
            if 'log.json' in file:
                logs.append(os.path.join(r, file))
            if 'label.json' in file:
                labels.append(os.path.join(r, file))
    try: 
        for i in range(len(logs)):
            log = json.loads(open(logs[i]).read())
            label = json.loads(open(labels[i]).read())
            for j in range(len(log["turns"])):
                print("System: ", log["turns"][j]["output"]["transcript"])
                print("User: ", label["turns"][j]["transcription"])
            print()
            not input("Press enter to continue")
    except KeyboardInterrupt:
        pass
    return
        
# Read the source data and write all dialogs in human readable format to a file named "dialogs.txt"
# Input:
# params: <<str>, <str>> dictionary, 
#         key = string for the relative path of the input root directory 'dstc2_traindev/data/'
#         value = string for the relative path of the output file 'dialogs.txt'
def saveAllDialogs(params):
    logs = []
    labels = []
    for r, d, f in os.walk(params["from"]):
        for file in f:
            if 'log.json' in file:
                logs.append(os.path.join(r, file))
            if 'label.json' in file:
                labels.append(os.path.join(r, file))
    f = open(params["to"], "w+")
    for i in range(len(logs)):
        log = json.loads(open(logs[i]).read())
        label = json.loads(open(labels[i]).read())
        for j in range(len(log["turns"])):
            f.write("System: " + log["turns"][j]["output"]["transcript"] + "\n")
            f.write("User: " + label["turns"][j]["transcription"] + "\n")
        f.write("\n")
    f.close()

if __name__ == "__main__":
    #TODO might need some adjustment
    myPath = './../dstc2_traindev/data' 
    myDict = {"from": "./../dstc2_traindev/data", "to": "./dialogs.txt"}
    displayAllDialogs(myPath)
    saveAllDialogs(myDict)
