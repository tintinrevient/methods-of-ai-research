import os, json, random

def prepareDataSet(from_dir, to_dir):
    """
    Prepare the dataset in the format 'dialog_act utterance_content'

    The dataset (i.e., the original training and test set combined) is split in a training part of 85% and a test part of 15%.

    Input: 
    from_dir: <str> the path of the input directory, e.g., the parent folder of 'dstc2_test' and 'dstc2_traindev'
    to_dir: <str> the path of the output directory
    """

    labels = []

    for r, d, f in os.walk(from_dir):
        for file in f:
            if 'label.json' in file:
                labels.append(os.path.join(r, file))

    train_file = open(os.path.join(to_dir, 'label_train_dialogs.txt'), "w+")
    test_file = open(os.path.join(to_dir, 'label_test_dialogs.txt'), "w+")

    # Shuffle the dataset
    random.shuffle(labels)

    split = int(len(labels) * 0.85)

    __generateDataSet(labels[:split], train_file)
    __generateDataSet(labels[split:], test_file)


def __generateDataSet(labels, f):
    """
    Generate the training file in the format: dialog_act utterance_content.

    There also exist multiple dialog_acts for one utterance_content, so the sentence is split into multiple lines of dialog_act utterance_content.

    Input:
    labels: [<str>] list of labels
    f: open file on which to write the data
    """

    for i in range(len(labels)):

        label = json.loads(open(labels[i]).read())

        for j in range(len(label["turns"])):

            label_acts_string = label["turns"][j]["semantics"]["cam"]

            # Remove the duplicates filtered from list to set
            label_acts_set = {"%s" % k[:k.index('(')] for k in label_acts_string.split('|')}
            label_transcription_string = label["turns"][j]["transcription"]

            for label_act in label_acts_set:
                f.write(label_act.lower() + " " + label_transcription_string.lower() + "\n")

        f.write("\n")

    f.close()

if __name__ == "__main__":

    # TODO might need some local adjustment
    from_dir = '../dstc2/'
    to_dir = '../label_dialogs/'

    prepareDataSet(from_dir, to_dir)