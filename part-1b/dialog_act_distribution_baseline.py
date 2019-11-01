import numpy

def utter(fileNames):
    """
    Predict the user dialog act using a distribution baseline
    Input:
    fileNames: [<str>] files containing dialog label data
    """
    model = __initModel(fileNames)

    print("Please enter your sentence...")

    try:
        while True:
            utterance = input()
            print(numpy.random.choice(list(model.keys()), 1, p=list(model.values()))[0])

    except KeyboardInterrupt:
        pass

def __initModel(fileNames):
    """
    Initialise the model based on the act distribution from the input files
    Input: 
    fileNames: [<str>] files containing dialog label data
    Output: model fit for classifying utterances
    """
    lines = []
    for fileName in fileNames:
        with open(fileName) as f:
            lines = lines + f.readlines()
    model = {
        'ack': 0,
        'affirm': 0,
        'bye': 0,
        'confirm': 0,
        'deny': 0,
        'hello': 0,
        'inform': 0,
        'negate': 0,
        'null': 0,
        'repeat': 0,
        'reqalts': 0,
        'reqmore': 0,
        'request': 0,
        'restart': 0,
        'thankyou': 0
    }
    sum = 0
    for line in lines:
        try:
            act = line[:line.index(" ")]
            try:
                model[act] = model[act] + 1
                sum = sum + 1
            except KeyError:
                pass
        except ValueError:
            pass
    for key in model.keys():
        model[key] = model[key] / sum
    return model

if __name__ == "__main__":
    # TODO might need some local adjustment
    fileNames = ['../dataset-txt/label_train_dialogs.txt',
                '../dataset-txt/label_test_dialogs.txt']
    utter(fileNames)