import numpy, yaml

def utter():
    """
    Predict the user dialog act using a distribution baseline
    """

    model = __initModel()

    print("Please enter your sentence...")

    try:
        while True:
            utterance = input()
            print(numpy.random.choice(list(model.keys()), 1, p=list(model.values()))[0])

    except KeyboardInterrupt:
        pass

def __initModel():
    """
    Initialise the model based on the act distribution from the input files
    """

    with open("config.yml", 'r') as file:
        config = yaml.load(file)

    lines = []

    for file in config["path"]["label_dialogs"]:
        with open(file) as f:
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

    utter()