
def utter():

    print("Please enter your sentence...")

    try:
        while True:
            utterance = input()
            print(__keywordMatching(utterance))

    except KeyboardInterrupt:
        pass

import collections
def __keywordMatching(utterance, repetition = False):

    dialog_acts = {}
    # Dialog acts keywords arrys
    ack_keywords = ["ackn", "ack"]
    affirm_keywords = ["affirm"]
    bye_keywords = ["bye"]
    confirm_keywords = ["confirm"]
    deny_keywords = ["deny"]
    hello_keywords = ["hello"]
    inform_keywords = ["inform"]
    negate_keywords = ["negate"]
    null_keywords = ["null"]
    repeat_keywords = ["repeat"]
    reqalts_keywords = ["reqalts"]
    reqmore_keywords = ["reqmore"]
    request_keywords = ["request"]
    restart_keywords = ["restart"]
    thankyou_keywords = ["thankyou"]
    
    dialog_acts["ack_keywords"] = ack_keywords
    dialog_acts["affirm_keywords"] = affirm_keywords
    dialog_acts["bye_keywords"] = bye_keywords
    dialog_acts["confirm_keywords"] = confirm_keywords
    dialog_acts["deny_keywords"] = deny_keywords
    dialog_acts["hello_keywords"] = hello_keywords
    dialog_acts["inform_keywords"] = inform_keywords
    dialog_acts["negate_keywords"] = negate_keywords
    dialog_acts["null_keywords"] = null_keywords
    dialog_acts["repeat_keywords"] = repeat_keywords
    dialog_acts["reqalts_keywords"] = reqalts_keywords
    dialog_acts["reqmore_keywords"] = reqmore_keywords
    dialog_acts["request_keywords"] = request_keywords
    dialog_acts["restart_keywords"] = restart_keywords
    dialog_acts["thankyou_keywords"] = thankyou_keywords

    utterance_keywords = utterance.split(" ")
    
    utterance_matches = {} #not really used but could be handy 
    utterance_matches_len = {}
    
    if repetition == False:
        for dialog_act in dialog_acts:
            matches = set(dialog_acts[dialog_act]).intersection(utterance_keywords)
            utterance_matches[dialog_act] = matches
            utterance_matches_len[dialog_act] = len(matches)
    else:
        for dialog_act in dialog_acts:
            matches = 0
            for keyword in dialog_acts[dialog_act]:
                matches = matches + utterance_keywords.count(keyword)
            utterance_matches[dialog_act] = set(dialog_acts[dialog_act]).intersection(utterance_keywords)
            utterance_matches_len[dialog_act] = matches
    max_matches = max(utterance_matches_len.values())
    dialog_matches = [ k for k, v in utterance_matches_len.items() if v == max_matches]
    
    return dialog_matches
    
    
    
if __name__ == "__main__":

    utter()