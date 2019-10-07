from keras.models import Sequential
from keras.layers.core import Activation, Dropout, Dense
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
from keras.utils import to_categorical
from keras.models import load_model
import yaml

def utter():
    """
    User types in random sentences, and the system will predict the user's act, a.k.a. intent.
    """

    with open("config.yml", 'r') as file:
        config = yaml.load(file, Loader=yaml.BaseLoader)

    model = load_model(config["path"]["model"])

    try:
        while True:
            print("Please enter your sentence...")

            utterance = input()

            tokenizer, encoder = load_tokenizer_and_encoder(config["path"]["label_dialogs"]["train"])

            prediction = model.predict(np.array(tokenizer.texts_to_matrix([utterance], mode='count')))

            print(encoder.classes_[np.argmax(prediction[0])])

    except KeyboardInterrupt:
        pass


def train_model():
    """
    This method can train the model based on the train file, and validate its accuracy by the test file.

    The model will be dumped to a model file, which can be imported and used during the utter() method.

    One-hot encoding is used for the word encoding.
    """

    with open("config.yml", 'r') as file:
        config = yaml.load(file, Loader=yaml.BaseLoader)

    tokenizer, encoder = load_tokenizer_and_encoder(config["path"]["label_dialogs"]["train"])

    train_labels, train_utterances = prepare_dataset(config["path"]["label_dialogs"]["train"])
    test_labels, test_utterances = prepare_dataset(config["path"]["label_dialogs"]["test"])

    # one-hot encoding
    x_train = tokenizer.texts_to_matrix(train_utterances, mode="count")
    x_test = tokenizer.texts_to_matrix(test_utterances)

    y_train = encoder.transform(train_labels)
    y_test = encoder.transform(test_labels)

    num_classes = np.max(y_train) + 1

    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    batch_size = int(config["batch_size"])
    epochs = int(config["epochs"])

    model = Sequential()
    model.add(Dense(512, input_shape=(int(config["max_words"]),)))
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

    model.save(config["path"]["model"])


def prepare_dataset(fileName):
    """
    Load the dataset into labels and utterances.
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


def load_tokenizer_and_encoder(fileName):
    """
    Load the tokenizer for the utterances and the encoder for the labels.
    """

    with open("config.yml", 'r') as file:
        config = yaml.load(file, Loader=yaml.BaseLoader)

    y, x = prepare_dataset(fileName)

    tokenizer = Tokenizer(num_words=int(config["max_words"]))
    tokenizer.fit_on_texts(x)

    encoder = LabelEncoder()
    encoder.fit(y)

    return tokenizer, encoder


if __name__ == "__main__":

    # Train the model as the first step
    # train_model()

    # Predict the user's act by the model
    utter()