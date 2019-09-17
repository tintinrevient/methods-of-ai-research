
def utter():

    print("Please enter your sentence...")

    try:
        while True:
            utterance = input()
            print(__keywordMatching(utterance))

    except KeyboardInterrupt:
        pass

def __keywordMatching(utterance):

    inform_keywords = ["looking", "want"]
    bye_keywords = ["bye"]
    thank_keywords = ["thank"]
    request_keywords = ["what"]
    deny_keywords = ["dont"]

    utterance = utterance.split(" ", 1)

    if len(set(bye_keywords).intersection(utterance)) >= 1:
        dialog_act = "bye"
    elif len(set(deny_keywords).intersection(utterance)) >= 1:
        dialog_act = "deny"
    elif len(set(thank_keywords).intersection(utterance)) >= 1:
        dialog_act = "thankyou"
    elif len(set(request_keywords).intersection(utterance)) >= 1:
        dialog_act = "request"
    elif len(set(inform_keywords).intersection(utterance)) >= 1:
        dialog_act = "inform"
    else:
        dialog_act = "noise"

    return dialog_act

if __name__ == "__main__":

    utter()