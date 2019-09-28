# -*- coding: utf-8 -*-

# Handlers for the different dialog acts
# Output: <str> next dialog state
# TODO
def ack():
    return "ack"
# TODO
def affirm():
    return "affirm"
# TODO
def bye():
    return "bye"
# TODO
def confirm():
    return "confirm"
# TODO
def deny():
    return "deny"
# TODO
def hello():
    return "hello"
# TODO
def inform():
    return "inform"
# TODO
def negate():
    return "negate"
# TODO
def null():
    return "null"
# TODO
def repeat():
    return "repeat"
# TODO
def requalts():
    return "requalts"
# TODO
def reqmore():
    return "reqmore"
# TODO
def request():
    return "request"
# TODO
def restart():
    return "restart"
# TODO
def thankyou():
    return "thankyou"
# TODO
def invalid_act():
    return "invalid_act"

# User dialog acts
dialog_acts = {
        "ack":ack,
        "affirm":affirm,
        "bye":bye,
        "confirm":confirm,
        "deny":deny,
        "hello":hello,
        "inform":inform,
        "negate":negate,
        "null":null,
        "repeat":repeat,
        "reqalts":requalts,
        "reqmore":reqmore,
        "request":request,
        "restart":restart,
        "thankyou":thankyou
}

# User preferences
preferences = {
        "food_type":"",
        "location":"",
        "price_range":""
}

# Find preferences missing user input
def preferences_not_set():
    not_set = []
    for parameter in preferences:
        if preferences[parameter] == "":
            not_set.extend(parameter)
    return not_set
# Restart preferences
def reset_preferences():
    for parameter in preferences:
        preferences[parameter] = ""
        
# Overwrite a preference. 
# Input:
# preference: <str> preference retrieved from the inform act
# value: <str> value retrieved from the inform act
# Output: <int> 0 if no problems, -1 if preference does not exist
    # This function might be unnecesary
def set_preference(preference, value):
    if preference in preferences:
        preferences[preference] = value
        return 0
    else:
        return -1


# Dialog state nodes utterances generation handlers
# Output: <str> next system utterance
#TODO
def welcome():
    return "welcome message"
# TODO
def inform_no_matches():
    return "inform_no_matchesmessage"
# Deleted, no point in having this dialog state
#def change_preferences():
#    return "change_preferences message"
# TODO
def request_missing_preferences():
    return "request_missing_preferences message"
# TODO
def suggest_restaurant():
    return "suggest_restaurant message"
# TODO
def provide_description():
    return "provide_description message"
# TODO
def provide_details():
    return "provide_details message"
# TODO
def closure():
    return "closure message"

# Dialog state nodes
system_states = {
        "welcome":welcome, 
        "inform_no_matches":inform_no_matches, 
#        "change_preferences":change_preferences, 
        "request_missing_preferences":request_missing_preferences, 
        "suggest_restaurant":suggest_restaurant,
        "provide_description":provide_description,
        "provide_details":provide_details,
        "closure":closure
}

# Determine state transition and system utterance
# Input:
# current_state: current dialog state
# current_input: current user utterance
# Output:
# <str>: next dialog state
# <str>: next system utterance
def dialog_transition(current_state, current_input):
    next_dialog_state = ""
    next_system_utterance = ""
    
    current_act = get_act(current_input)
    if current_act == "inform":
        extract_information(current_input)
    next_dialog_state = next_state(current_state, current_act)
    next_system_utterance = generate_utterance(next_dialog_state)
    return next_dialog_state, next_system_utterance


# Extract the dialog act from the user utterance
# Input: 
# utterance: current user utterance
# Output: <str> dialog act identified
def get_act(utterance):
    #TODO
    act = ""
    return act

# Extract the relevant information from the current input
# Input:
# utterance: <str> current user utterance classified as inform
def extract_information(utterance):
    #TODO
    return

# Decide what the next state should be based on current state and dialog act
# Input
# current_state: <str> current dialog state
# current_act: <str> dialog act extracted from the user input
# Output: <str> next dialog state
def next_state(current_state, current_act):
    next_state = ""
    handler = dialog_acts.get(current_act, "invalid")
    # Refer to "Handlers for the different dialog acts"
    if handler == "invalid":
        print("Something went terribly wrong. We shouldn't have reached here!")
        next_state = "closure" # report bug
    else:
        next_state = handler()
    return next_state

# Build the next utterance based on the current state of the dialog
# Input:
# state: <str> next dialog state
# Output: <str> next system utterance
def generate_utterance(state):
    utterance = ""
    handler = system_states.get(state, "invalid")
    # Refer to "Handlers for the different dialog acts"
    if handler == "invalid":
        print("Something went terribly wrong. We shouldn't have reached here!")
        utterance = "An error occurred. Report dialog log" # report bug
    else:
        utterance = handler()
    return utterance


# Start a dialog
def init_dialog():
    reset_preferences()
    print("Welcome to the restaurant selection assistant")
    current_state = "welcome"
    next_state = ""
    next_system_utterance = ""
    try:
        while True:
            current_input = input()
            next_state, next_system_utterance = dialog_transition(current_state, current_input)
            current_state = next_state
            print(next_system_utterance)

    except KeyboardInterrupt:
        pass