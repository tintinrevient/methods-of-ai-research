import os, json, random

def prepareDataSet(from_dir, to_dir):
    """
    Prepare the dataset in the format 'dialog_act utterance_content'

    The dataset (i.e., the original training and test set combined) is split in a training part of 85% and a test part of 15%.

    'from_dir' is a string for the absolute path of the input directory, e.g., the parent folder of 'dstc2_test' and 'dstc2_traindev'
    'to_dir' is a string for the absolute path of the output directory
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

    from_dir = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/'
    to_dir = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1b/'

    prepareDataSet(from_dir, to_dir)