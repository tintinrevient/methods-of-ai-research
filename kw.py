def keywordMatching(utterance):

    keyword = ["bye", "dont", "thank", "what", "looking"]
    inform_keywords = ["looking", "want"]

    if keyword[0] in utterance:
        dialog_act = "bye"
    elif keyword[1] in utterance:
        dialog_act = "deny"
    elif keyword[2] in utterance:
        dialog_act = "thankyou"
    elif keyword[3] in utterance:
        dialog_act = "request"
    elif keyword[4] in utterance:
        dialog_act = "inform"
    else:
        dialog_act = "noise"

    return dialog_act

sentence = " the post code"

print(keywordMatching(sentence))
