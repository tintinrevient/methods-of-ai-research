import os, json, yaml

def display_dialogs():
    """
    Read the source data and display the dialogs one by one in human-readable format.
    Use the Enter key to proceed to the next dialog.
    Use <KeyboardInterrupt> (Ctr+C) to escape
    """

    logs, labels = __load()

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

def save_dialogs(filename):
    """
    Read the source data and write all dialogs in human readable format to a file
    """
    
    logs, labels = __load()

    f = open(filename, "w+")

    for i in range(len(logs)):
        log = json.loads(open(logs[i]).read())
        label = json.loads(open(labels[i]).read())
        for j in range(len(log["turns"])):
            f.write("System: " + log["turns"][j]["output"]["transcript"] + "\n")
            f.write("User: " + label["turns"][j]["transcription"] + "\n")
        f.write("\n")
    f.close()

def __load():

    with open("config.yml", 'r') as file:
        config = yaml.load(file)

    logs = []
    labels = []

    for r, d, f in os.walk(config["path"]["dataset"]):
        for file in f:
            if 'log.json' in file:
                logs.append(os.path.join(r, file))
            if 'label.json' in file:
                labels.append(os.path.join(r, file))

    return logs, labels

if __name__ == "__main__":

    display_dialogs()