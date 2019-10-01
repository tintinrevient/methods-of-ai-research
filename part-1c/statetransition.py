from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
from keras.models import load_model

# maximum words to use as a dictionary
max_words = 1000

def utter(modelFile, trainFileName):

    model = load_model(modelFile)

    print("Hello, welcome to the Cambridge restaurant system. You can ask for restaurants by area, price range or food type. How may I help you?")

    try:
        while True:
            utterance = input()

            tokenizer, encoder = __loadTokenizerAndEncoder(trainFileName)
            prediction = model.predict(np.array(tokenizer.texts_to_matrix([utterance], mode='count')))

            print(encoder.classes_[np.argmax(prediction[0])])

    except KeyboardInterrupt:
        pass


def __prepareDataSet(fileName):
    """
    Load the dataset into labels and utterances.

    :param fileName:
    :return:
    """

    labels = []
    utterances = []

    with open(fileName) as f:
        lines = f.readlines()

    for line in lines:
        try:
            act = line[:line.index(" ")]
            utterance = line[line.index(" "):line.index("\n")]

            try:
                labels.append(act.strip())
                utterances.append(utterance.strip())

            except KeyError:
                pass

        except ValueError:
            pass

    return labels, utterances


def __loadTokenizerAndEncoder(fileName):

    y, x = __prepareDataSet(fileName)

    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(x)

    encoder = LabelEncoder()
    encoder.fit(y)

    return tokenizer, encoder


if __name__ == "__main__":

    trainFileName = '/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1b/dataset-txt/label_train_dialogs.txt'
    modelFile = '/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1b/model/dcnn_model.h5'

    # Train the model as the first step
    # trainModel(trainFileName, testFileName, modelFile)

    # Predict the user's act by the model
    utter(modelFile, trainFileName)