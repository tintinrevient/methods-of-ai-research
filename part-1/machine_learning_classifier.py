from keras.models import Sequential
from keras.layers.core import Activation, Dropout, Dense
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
from keras.utils import to_categorical
from keras.models import load_model

# maximum words to use as a dictionary
max_words = 1000

def utter(modelFile, trainFileName):
    """
    User types in random sentences, and the system will predict the user's act, a.k.a. intent.

    This method can only be successfully called by the already-trained DCNN model.

    Input:
    modelFile: <str> path to the model file
    trainFileName: <str> path to the file containing training dialog data
    """

    model = load_model(modelFile)

    print("Please enter your sentence...")

    try:
        while True:
            utterance = input()

            tokenizer, encoder = __loadTokenizerAndEncoder(trainFileName)
            prediction = model.predict(np.array(tokenizer.texts_to_matrix([utterance], mode='count')))

            print(encoder.classes_[np.argmax(prediction[0])])

    except KeyboardInterrupt:
        pass


def trainModel(trainFileName, testFileName, modelFile):
    """
    This method can train the DCNN model based on the train file, and validate its accuracy by the test file.

    The model will be dumped to a model file, which can be imported and used during the utter() method.

    One-hot encoding is used for the word encoding.

    Input:
    trainFileName: <str> path to the file containing training dialog data
    testFileName: <str> path to the file containing testing dialog data
    modelFile: path to the model file
    """

    tokenizer, encoder = __loadTokenizerAndEncoder(trainFileName)

    train_labels, train_utterances = __prepareDataSet(trainFileName)
    test_labels, test_utterances = __prepareDataSet(testFileName)

    # one-hot encoding
    x_train = tokenizer.texts_to_matrix(train_utterances, mode="count")
    x_test = tokenizer.texts_to_matrix(test_utterances)

    y_train = encoder.transform(train_labels)
    y_test = encoder.transform(test_labels)

    num_classes = np.max(y_train) + 1

    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    batch_size = 32
    epochs = 10

    model = Sequential()
    model.add(Dense(512, input_shape=(max_words,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    print(model.summary())

    history = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1,
                        validation_split=0.1)

    score = model.evaluate(x_test, y_test, verbose=1)
    print("\n score:", score)

    model.save(modelFile)


def __prepareDataSet(fileName):
    """
    Load the dataset into labels and utterances.

    Inpur: 
    fileName: <str> path to the file containing dialog data
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
    """
    Load the tokenizer for the utterances and the encoder for the labels.

    Input: 
    fileName: <str> path to the file containing dialog data
    """

    y, x = __prepareDataSet(fileName)

    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(x)

    encoder = LabelEncoder()
    encoder.fit(y)

    return tokenizer, encoder



if __name__ == "__main__":

    # TODO might need some local adjustment
    trainFileName = '../dataset-txt/label_train_dialogs.txt'
    testFileName = '../dataset-txt/label_test_dialogs.txt'
    modelFile = '../model/dcnn_model.h5'

    # Train the model as the first step
    trainModel(trainFileName, testFileName, modelFile)

    # Predict the user's act by the model
    utter(modelFile, trainFileName)