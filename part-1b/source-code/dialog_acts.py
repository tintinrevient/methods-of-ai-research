import os, json, random

def prepareDataSet(from_dir, to_dir):
    """
    Prepare the dataset in the format 'dialog_act utterance_content'

    The dataset (i.e., the original training and test set combined) is split in a training part of 85% and a test part of 15%.

    'from_dir' is a string for the absolute path of the input directory, e.g., the parent folder of 'dstc2_test' and 'dstc2_traindev'
    'to_dir' is a string for the absolute path of the output directory
    """

    logs = []
    labels = []

    for r, d, f in os.walk(from_dir):
        for file in f:
            if 'log.json' in file:
                logs.append(os.path.join(r, file))
            if 'label.json' in file:
                labels.append(os.path.join(r, file))

    train_file = open(os.path.join(to_dir, 'label_train_dialogs.txt'), "w+")
    test_file = open(os.path.join(to_dir, 'label_test_dialogs.txt'), "w+")

    split = int(len(logs) * 0.85)

    __generateDataSet(logs[:split], labels[:split], train_file)
    __generateDataSet(logs[split:], labels[split:], test_file)


def __generateDataSet(logs, labels, f):
    for i in range(len(logs)):
        log = json.loads(open(logs[i]).read())
        label = json.loads(open(labels[i]).read())

        for j in range(len(log["turns"])):
            # log_acts_array = log["turns"][j]["output"]["dialog-acts"]
            # log_acts_set = {"%s" % log_acts_array[k]["act"] for k in range(len(log_acts_array))}
            # log_transcript_string = log["turns"][j]["output"]["transcript"]
            #
            # for log_act in log_acts_set:
            #     f.write(log_act.lower() + " " + log_transcript_string.lower() + "\n")

            # Only generate the dataset of user's dialog acts, as it is the dataset to be used in the training phase
            label_acts_string = label["turns"][j]["semantics"]["cam"]

            # Remove the duplicates filtered from list to set
            label_acts_set = {"%s" % k[:k.index('(')] for k in label_acts_string.split('|')}
            label_transcription_string = label["turns"][j]["transcription"]

            for label_act in label_acts_set:
                f.write(label_act.lower() + " " + label_transcription_string.lower() + "\n")

        f.write("\n")

    f.close()

if __name__ == "__main__":

    from_dir = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/'
    to_dir = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1b/'

    prepareDataSet(from_dir, to_dir)