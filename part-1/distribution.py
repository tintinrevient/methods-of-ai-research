import numpy, yaml

def utter():
    """
    Predict the user dialog act using a distribution baseline
    """

    model = init_model()

    feedback = {
        "count": 0,
        "yes": 0,
        "no": 0
    }

    try:
        while True:
            print("Please enter your sentence...")

            utterance = input()
            print(numpy.random.choice(list(model.keys()), 1, p=list(model.values()))[0])

            print("Is the predicted act correct? Please enter 'yes' or 'no':")

            answer = input()

            if answer == "yes":
                feedback["yes"] += 1
            elif answer == "no":
                feedback["no"] += 1

            feedback["count"] += 1

    except KeyboardInterrupt:

        error_rate = feedback["yes"] / feedback["count"]
        print("Thanks for your feedback and the error rate is {:4.2f} %".format(error_rate*100))

        pass


def init_model():
    """
    Initialise the model based on the act distribution from the input files
    """

    with open("config.yml", 'r') as file:
        config = yaml.load(file, Loader=yaml.BaseLoader)

    lines = []

    for file in [config["path"]["label_dialogs"]["train"], config["path"]["label_dialogs"]["test"]]:
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