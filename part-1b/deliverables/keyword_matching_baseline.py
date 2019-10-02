
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
    # Dialog acts keywords arrays
    ack_keywords = ["okay", "kay", "well", "great", "fine", "good", "thatll", "do"]
    affirm_keywords = ["yea", "yes", "correct", "right", "ye", "perfect", "yeah"]
    bye_keywords = ["goodbye", "bye"]
    confirm_keywords = ["is", "are", "they", "does", "do"] # always a question about the service (does it, do they, is it, are they). We omit 'it' for reasons
    deny_keywords = ["dont", "wrong", "no", "not", "change"]
    hello_keywords = ["hello", "hi", "halo"]
    negate_keywords = ["no"]
    null_keywords = [] # default to anything else
    repeat_keywords = ["repeat", "back", "again"]
    reqalts_keywords = ["another", "about", "else"] #nonexistent in training data
    reqmore_keywords = ["more"]
    restart_keywords = ["start", "over", "reset", "restart"]
    thankyou_keywords = ["thanks", "thank"]
    # May be a question requesting (can i, may i, what is...)
    request_keywords = [] 
    request_details_keywords = ["much", "phone", "number", "postcode", "post", "code", "address", "type", "kind", "price", "range", "area", "telephone"]
    request_question_keywords = ["how", "whats", "what", "can", "may", "could", "need"]
    request_keywords.extend(request_details_keywords)
    request_keywords.extend(request_question_keywords)
    #We will need a special set of words for this set
    inform_food_type_keywords = ["thai", "chinese", "gastropub", "cuban", "seafood", "canapes", "indian", "african", "catalan", "turkish", "venetian", "porguguese", "oriental", "hungarian", "mediterranean", "creative", "asian", "traditional", "unusual", "malaysian", "jamaican", "french", "italian", "european", "american", "persian", "moroccan", "british", "korean", "romanian", "polish", "japanese", "english", "christmas", "barbecue", "cantonese", "spanish", "lebanese", "swedish", "mexican", "caribbean", "danish", "irish", "corsica", "afghan", "australian", "russian", "polynesian", "world", "kosher", "vegetarian", "tuscan", "scandinavian", "basque", "german", "persian", "eritrean", "austrian", "singaporean", "swiss", "scottish", "bistro", "welsh", "brazilian", "fusion", "steak", "pub", "halal", "gastro", "belgian", "steakhouse"]
    inform_price_range_keywords = ["cheap", "moderately", "moderate", "priced", "expensive"]
    inform_area_keywords = ["south", "north", "east", "west", "center", "anywhere"]
    
    inform_keywords = ["any", "kind", "food", "restaurant", "town", "part", "looking", "for", "dont", "care", "doesnt", "matter"] 
    inform_keywords.extend(inform_food_type_keywords)
    inform_keywords.extend(inform_price_range_keywords)
    inform_keywords.extend(inform_area_keywords)
    
    
    
    
    
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
