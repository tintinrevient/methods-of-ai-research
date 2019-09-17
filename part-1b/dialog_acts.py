import os, json, re

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
            log_acts_array = log["turns"][j]["output"]["dialog-acts"]
            log_acts_set = {"%s" % log_acts_array[k]["act"] for k in range(len(log_acts_array))}
            log_transcript_string = log["turns"][j]["output"]["transcript"]

            for log_act in log_acts_set:
                print("System: (" + log_act.lower() + ") " + log_transcript_string.lower())

            label_acts_string = label["turns"][j]["semantics"]["cam"]
            label_acts_set = {"%s" % k[:k.index('(')] for k in label_acts_string.split('|')}
            label_transcription_string = label["turns"][j]["transcription"]

            for label_act in label_acts_set:
                print("User: (" + label_act.lower() + ") " + label_transcription_string.lower())

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
            log_acts_array = log["turns"][j]["output"]["dialog-acts"]
            log_acts_set = {"%s" % log_acts_array[k]["act"] for k in range(len(log_acts_array))}
            log_transcript_string = log["turns"][j]["output"]["transcript"]

            for log_act in log_acts_set:
                f.write("System: (" + log_act.lower() + ") " + log_transcript_string.lower() + "\n")

            label_acts_string = label["turns"][j]["semantics"]["cam"]
            label_acts_set = {"%s" % k[:k.index('(')] for k in label_acts_string.split('|')}
            label_transcription_string = label["turns"][j]["transcription"]

            for label_act in label_acts_set:
                f.write("User: (" + label_act.lower() + ") " + label_transcription_string.lower() + "\n")

        f.write("\n")

    f.close()

if __name__ == "__main__":
    myPath = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/'

    # Display All Dialogs
    # displayAllDialogs(myPath)


    # Save All Dialogs
    params = {"from": "/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/",
              "to": "/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1b/dialog_acts.txt"}
    saveAllDialogs(params)