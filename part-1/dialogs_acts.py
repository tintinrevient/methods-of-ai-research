import os, json, random, yaml

def produce_act_dialogs():
    """
    Prepare the dataset in the format 'dialog_act utterance_content'

    The dataset (i.e., the original training and test set combined) is split in a training part of 85% and a test part of 15%.
    """

    with open("config.yml", 'r') as file:
        config = yaml.load(file, Loader=yaml.BaseLoader)

    labels = []

    for r, d, f in os.walk(config["path"]["dataset"]):
        for file in f:
            if 'label.json' in file:
                labels.append(os.path.join(r, file))

    train_file = open(config["path"]["label_dialogs"]["train"], "w+")
    test_file = open(config["path"]["label_dialogs"]["test"], "w+")

    # Shuffle the dataset
    random.shuffle(labels)

    split = int(len(labels) * 0.85)

    save_act_dialogs(labels[:split], train_file)
    save_act_dialogs(labels[split:], test_file)


def save_act_dialogs(labels, file):
    """
    Generate the training file in the format: dialog_act utterance_content.

    There also exist multiple dialog_acts for one utterance_content, so the sentence is split into multiple lines of dialog_act utterance_content.
    """

    for i in range(len(labels)):

        label = json.loads(open(labels[i]).read())

        for j in range(len(label["turns"])):

            label_acts_string = label["turns"][j]["semantics"]["cam"]

            # Remove the duplicates filtered from list to set
            label_acts_set = {"%s" % k[:k.index('(')] for k in label_acts_string.split('|')}
            label_transcription_string = label["turns"][j]["transcription"]

            for label_act in label_acts_set:
                file.write(label_act.lower() + " " + label_transcription_string.lower() + "\n")

        file.write("\n")

    file.close()

if __name__ == "__main__":

    produce_act_dialogs()