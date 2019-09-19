def keywordMatching(utterance):

    inform_keywords = ["looking", "want", "find", "food"]
    bye_keywords = ["bye"]
    thank_keywords = ["thank"]
    request_keywords = ["what", "number", "code", "address"]
    deny_keywords = ["dont"]
    hello_keywords = ["hi", "hello"]
    acknowledgment_keywords = ["okay"]
    reqalts_keywords = ["how"]
    negate_keywords = ["no"]
    affirm_keywords = ["yes"]

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
    elif len(set(hello_keywords).intersection(utterance)) >= 1:
        dialog_act = "hello"
    elif len(set(acknowledgment_keywords).intersection(utterance)) >= 1:
        dialog_act = "ack"
    elif len(set(reqalts_keywords).intersection(utterance)) >= 1:
        dialog_act = "reqalts"
    elif len(set(negate_keywords).intersection(utterance)) >= 1:
        dialog_act = "negate"
    elif len(set(affirm_keywords).intersection(utterance)) >= 1:
        dialog_act = "affirm"
    else:
        dialog_act = "null"

    return dialog_act

sentence = "what is the post code"

print(keywordMatching(sentence))
