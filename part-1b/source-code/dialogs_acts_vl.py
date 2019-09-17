"""
PART 1b
"""
import os, json
def displayAllUtterances(path):

    """
    Read the source data and display the dialogs one by one in human-readable format.
    Use the Enter key to proceed to the next dialog.

    Input parameter 'path' is a string for the absolute path of the input root directory 'dstc2_traindev/data/'.
    """

    labels = []

    for r, d, f in os.walk(path):
        for file in f:
            if 'label.json' in file:
                labels.append(os.path.join(r, file))

    for i in range(len(logs)):
        label = json.loads(open(labels[i]).read())

        for j in range(len(log["turns"])):
            label_dialog_acts = label["turns"][j]["semantics"]["cam"].split('|')
            for k in range(len(label_dialog_acts)):
                print("(" + label_dialog_acts[k].split('(')[0] + ") " + label["turns"][j]["transcription"])
        print()
        not input("Press enter to continue")




def saveAllUtterances(params):

    """
    Read the source data and write all dialogs in human readable format to a file named "dialogs.txt"

    Input parameter 'params' is a dictionary of the format {'from': '/...', 'to': '/...'}
    'from' is a string for the absolute path of the input root directory 'dstc2_traindev/data/'
    'to' is a string for the absolute path of the output file 'dialogs.txt'
    """

    labels = []

    for r, d, f in os.walk(params["from"]):
        for file in f:
            if 'label.json' in file:
                labels.append(os.path.join(r, file))

    f = open(params["to"], "w+")

    for i in range(len(labels)):
        label = json.loads(open(labels[i]).read())

        for j in range(len(label["turns"])):
            label_dialog_acts = label["turns"][j]["semantics"]["cam"].split('|')
            for k in range(len(label_dialog_acts)):
                f.write("(" + label_dialog_acts[k].split('(')[0] + ") " + label["turns"][j]["transcription"].lower())
                f.write("\n")
    f.close()
    
    
import random
def shuffleFileContents(file_in, file_out):
    f_in = open(file_in, "r")
    data = [ (random.random(), line) for line in f_in]
    data.sort()
    f_out = open(file_out, "w+")
    for _, line in data:
        f_out.write(line)
    f_in.close()
    f_out.close()
    
import math
def splitContents(file, split):
    # 0 <= split <= 1
    f = open(file, "r")
    path = os.path.dirname(file)
    basename = os.path.basename(file)
    f_lines = f.readlines()
    split_line = math.floor(len(f_lines)*split)
    with open(path + "/" + str(math.floor(split*100)) + "_" + basename, "w+") as f1:
        f1.writelines(f_lines[:split_line])
    with open(path + "/" + str(math.floor((1-split)*100)) + "_" + basename, "w+") as f2:
        f2.writelines(f_lines[split_line:])
    f.close()
    
