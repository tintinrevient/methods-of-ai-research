from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense, Activation
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import one_hot
from keras.utils import to_categorical

def trainModel(trainFileName, testFileName):

    vocabulary_size = 1000

    # Prepare the training dataset
    train_labels, train_utterances = prepareDataSet(trainFileName)
    train_encoded_utterances = [one_hot(utterance, vocabulary_size) for utterance in train_utterances]
    train_padded_utterances = pad_sequences(train_encoded_utterances, maxlen = 10)

    train_encoded_labels = [one_hot(label, 15) for label in train_labels]
    train_categorical_labels = to_categorical(train_encoded_labels, num_classes=15)

    # print(train_categorical_labels.shape)

    # Prepare the test dataset
    test_labels, test_utterances = prepareDataSet(testFileName)
    test_encoded_utterances = [one_hot(utterance, vocabulary_size) for utterance in test_utterances]
    test_padded_utterances = pad_sequences(test_encoded_utterances, maxlen = 10)

    test_encoded_labels = [one_hot(label, 15) for label in test_labels]
    test_categorical_labels = to_categorical(test_encoded_labels, num_classes=15)

    model = Sequential()

    model.add(Embedding(vocabulary_size, 64, input_shape=(10,)))
    model.add(Flatten())
    model.add(Dense(15, activation='softmax'))
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])

    print(model.summary())

    model.fit(train_padded_utterances, train_categorical_labels, epochs=5, verbose=1)

    # Evaluate the loss and accuracy by the test dataset
    loss, accuracy = model.evaluate(test_padded_utterances, test_categorical_labels, verbose=1)
    print(loss, accuracy)

    # input_array = ['what is the address']
    # output_array = model.predict(input_array)
    # print(output_array)

def prepareDataSet(fileName):

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


if __name__ == "__main__":

    trainFileName = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1b/label_train_dialogs.txt'
    testFileName = '/Users/zhaoshu/Documents/courses/Methods_of_AI_Research/lab-assignments/part-1b/label_test_dialogs.txt'

    trainModel(trainFileName, testFileName)