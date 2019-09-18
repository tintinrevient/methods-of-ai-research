from keras.models import Sequential
from keras.layers.core import Activation, Dropout, Dense
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
from keras import utils
from keras.models import load_model

max_words = 1000

def trainModel(trainFileName, testFileName, modelFile):

    tokenizer, encoder = __loadTokenizerAndEncoder(trainFileName)

    train_labels, train_utterances = __prepareDataSet(trainFileName)
    test_labels, test_utterances = __prepareDataSet(testFileName)

    x_train = tokenizer.texts_to_matrix(train_utterances, mode="count")
    x_test = tokenizer.texts_to_matrix(test_utterances)

    y_train = encoder.transform(train_labels)
    y_test = encoder.transform(test_labels)

    num_classes = np.max(y_train) + 1

    y_train = utils.to_categorical(y_train, num_classes)
    y_test = utils.to_categorical(y_test, num_classes)

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


def utter(modelFile, trainFileName):

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


def __prepareDataSet(fileName):

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

    trainFileName = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1b/label_train_dialogs.txt'
    testFileName = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1b/label_test_dialogs.txt'
    modelFile = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1b/dcnn_model.h5'

    # Train the model as the first step
    # trainModel(trainFileName, testFileName, modelFile)

    # Predict the user's act by the model
    utter(modelFile, trainFileName)