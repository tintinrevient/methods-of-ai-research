import os, json

def displayAllDialogs(path):

    """
    Read the source data and display the dialogs one by one in human-readable format.
    Use the Enter key to proceed to the next dialog.

    Input parameter 'path' is a string for the absolute path of the input root directory 'dstc2_traindev/data/'.
    """

    logs = []
    labels = []

    for r, d, f in os.walk(path):
        for file in f:
            if 'log.json' in file:
                logs.append(os.path.join(r, file))
            if 'label.json' in file:
                labels.append(os.path.join(r, file))

    for i in range(len(logs)):
        log = json.loads(open(logs[i]).read())
        label = json.loads(open(labels[i]).read())

        for j in range(len(log["turns"])):
            print("System: ", log["turns"][j]["output"]["transcript"])
            print("User: ", label["turns"][j]["transcription"])

        print()
        not input("Press enter to continue")


def saveAllDialogs(params):

    """
    Read the source data and write all dialogs in human readable format to a file named "dialogs.txt"

    Input parameter 'params' is a dictionary of the format {'from': '/...', 'to': '/...'}
    'from' is a string for the absolute path of the input root directory 'dstc2_traindev/data/'
    'to' is a string for the absolute path of the output file 'dialogs.txt'
    """

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
    myPath = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1a/dstc2_traindev/data'
    displayAllDialogs(myPath)
