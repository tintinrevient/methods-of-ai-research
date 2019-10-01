# -*- coding: utf-8 -*-


ACK_ACT = "ack"
AFFIRM_ACT = "affirm"
BYE_ACT = "bye"
CONFIRM_ACT = "confirm"
DENY_ACT = "deny"
HELLO_ACT = "hello"
INFORM_ACT = "inform"
NEGATE_ACT = "negate"
NULL_ACT = "null"
REPEAT_ACT = "repeat"
REQUALTS_ACT = "requalts"
REQMORE_ACT = "reqmore"
REQUEST_ACT = "request"
RESTART_ACT = "restart"
THANKYOU_ACT = "thankyou"
INVALIDACT_ACT = "invalid_act"

WELCOME_STATE = "welcome"
INFORM_NO_MATCHES_STATE = "inform_no_matches"
#        change_preferences_state = change_preferences""
REQUEST_MISSING_PREFERENCES_STATE = "request_missing_preferences"
SUGGEST_RESTAURANT_STATE = "suggest_restaurant"
PROVIDE_DESCRIPTION_STATE = "provide_description"
PROVIDE_DETAILS_STATE = "provide_details"
CLOSURE_STATE = "closure"
INVALIDSTATE_STATE = "invalid_state"

# Handlers for the different dialog acts
# Output: <str> next dialog state
# TODO should we move at all with this act?
def ack(current_state):
    if (current_state == WELCOME_STATE):
        # Don't transition
        next_state = WELCOME_STATE
    elif (current_state == INFORM_NO_MATCHES_STATE):
        # Don't transition
        next_state = INFORM_NO_MATCHES_STATE
    elif (current_state == REQUEST_MISSING_PREFERENCES_STATE):
        # Don't transition
        next_state = REQUEST_MISSING_PREFERENCES_STATE
    elif (current_state == SUGGEST_RESTAURANT_STATE):
        # Don't transition
        next_state = SUGGEST_RESTAURANT_STATE
    elif (current_state == PROVIDE_DESCRIPTION_STATE):
        # Don't transition
        next_state = PROVIDE_DESCRIPTION_STATE
    elif (current_state == PROVIDE_DETAILS_STATE):
        # Don't transition
        next_state = PROVIDE_DETAILS_STATE
    elif (current_state == CLOSURE_STATE):
        # Don't transition
        next_state = CLOSURE_STATE
    else:
        print("Generic error message generated when transitioning states")
        next_state = CLOSURE_STATE
    return next_state
# TODO should we move at all with this act?
def affirm(current_state):
    if (current_state == WELCOME_STATE):
        # Don't transition
        next_state = WELCOME_STATE
    elif (current_state == INFORM_NO_MATCHES_STATE):
        # Don't transition
        next_state = INFORM_NO_MATCHES_STATE
    elif (current_state == REQUEST_MISSING_PREFERENCES_STATE):
        # Don't transition
        next_state = REQUEST_MISSING_PREFERENCES_STATE
    elif (current_state == SUGGEST_RESTAURANT_STATE):
        # Don't transition
        next_state = SUGGEST_RESTAURANT_STATE
    elif (current_state == PROVIDE_DESCRIPTION_STATE):
        # Don't transition
        next_state = PROVIDE_DESCRIPTION_STATE
    elif (current_state == PROVIDE_DETAILS_STATE):
        # Don't transition
        next_state = PROVIDE_DETAILS_STATE
    elif (current_state == CLOSURE_STATE):
        # Don't transition
        next_state = CLOSURE_STATE
    else:
        print("Generic error message generated when transitioning states")
        next_state = CLOSURE_STATE
    return next_state

def bye(current_state):
    next_state = CLOSURE_STATE
    return next_state

def confirm(current_state):
    if (current_state == WELCOME_STATE):
        # Don't transition
        next_state = WELCOME_STATE
    elif (current_state == INFORM_NO_MATCHES_STATE):
        # Don't transition
        next_state = INFORM_NO_MATCHES_STATE
    elif (current_state == REQUEST_MISSING_PREFERENCES_STATE):
        # Don't transition 
        next_state = REQUEST_MISSING_PREFERENCES_STATE
    elif (current_state == SUGGEST_RESTAURANT_STATE):
        # Query description of the restaurant
        next_state = PROVIDE_DESCRIPTION_STATE
    elif (current_state == PROVIDE_DESCRIPTION_STATE):
        # Don't transition
        next_state = PROVIDE_DESCRIPTION_STATE
    elif (current_state == PROVIDE_DETAILS_STATE):
        # Don't transition
        next_state = PROVIDE_DETAILS_STATE
    elif (current_state == CLOSURE_STATE):
        # Don't transition(?)
        next_state = CLOSURE_STATE
    else:
        print("Generic error message generated when transitioning states")
        next_state = CLOSURE_STATE
    return next_state
# TODO
def deny(current_state):
    if (current_state == WELCOME_STATE):
        # The program was opened by mistake, we take
        next_state = CLOSURE_STATE
    elif (current_state == INFORM_NO_MATCHES_STATE):
        # Don't transition
        next_state = INFORM_NO_MATCHES_STATE
    elif (current_state == REQUEST_MISSING_PREFERENCES_STATE):
        # Don't transition 
        next_state = REQUEST_MISSING_PREFERENCES_STATE
    elif (current_state == SUGGEST_RESTAURANT_STATE):
        # TODO
        # TODO Extract relevant information
        # TODO update preferences if no updates this is actually requalts
        # Check preferences again and act accordingly
        if (len(preferences_not_set())>0): # We could land here, not redundant
            next_state = REQUEST_MISSING_PREFERENCES_STATE
        else:
            # Perform the lookup of restaurants in the db
            g_available_restaurants = find_possible_restaurants()
            # Check for availability
            if len(g_available_restaurants==0):
                next_state = INFORM_NO_MATCHES_STATE
            else:
                next_state = SUGGEST_RESTAURANT_STATE
        next_state = SUGGEST_RESTAURANT_STATE
    elif (current_state == PROVIDE_DESCRIPTION_STATE):
        #TODO like SUGGEST_RESTAURANT_STATE?
        next_state = PROVIDE_DESCRIPTION_STATE
    elif (current_state == PROVIDE_DETAILS_STATE):
        #TODO like SUGGEST_RESTAURANT_STATE?
        next_state = PROVIDE_DETAILS_STATE
    elif (current_state == CLOSURE_STATE):
        # Don't transition(?)
        next_state = CLOSURE_STATE
    else:
        print("Generic error message generated when transitioning states")
        next_state = CLOSURE_STATE
    return next_state

def hello(current_state):
    # Don't transition ever(?)
    return current_state
# After an inform act only no matches or suggest are possible states
# Moreover, inform act can be input from any other state
def inform(current_state):
    if (current_state == CLOSURE_STATE):
        # Don't transition(?)
        next_state = CLOSURE_STATE
    else:
        # Check constraints
        # CONFIGURATION POINT
        if (len(preferences_not_set())>0):
            next_state = REQUEST_MISSING_PREFERENCES_STATE
        else:
            # Perform the lookup of restaurants in the db
            g_available_restaurants = find_possible_restaurants()
            # Check for availability
            if len(g_available_restaurants==0):
                next_state = INFORM_NO_MATCHES_STATE
            else:
                next_state = SUGGEST_RESTAURANT_STATE
    return next_state
# TODO
def negate(current_state):
    if (current_state == WELCOME_STATE):
        # Don't transition(?)
        next_state = WELCOME_STATE
    elif (current_state == INFORM_NO_MATCHES_STATE):
        # Don't transition(?)
        next_state = INFORM_NO_MATCHES_STATE
    elif (current_state == REQUEST_MISSING_PREFERENCES_STATE):
        # Don't transition(?)
        next_state = REQUEST_MISSING_PREFERENCES_STATE
    elif (current_state == SUGGEST_RESTAURANT_STATE):
        # TODO This is actually requalts
        next_state = SUGGEST_RESTAURANT_STATE
    elif (current_state == PROVIDE_DESCRIPTION_STATE):
        # TODO This is actually inform
        next_state = PROVIDE_DESCRIPTION_STATE
    elif (current_state == PROVIDE_DETAILS_STATE):
        #TODO This is actually inform
        next_state = PROVIDE_DETAILS_STATE
    elif (current_state == CLOSURE_STATE):
        # Don't transition(?)
        next_state = CLOSURE_STATE
    else:
        print("Generic error message generated when transitioning states")
        next_state = CLOSURE_STATE
    return next_state
# Don't transition ever, just repeat
def null(current_state):
    return current_state
# Don't transition ever, just repeat
def repeat(current_state):
    return current_state
# TODO like inform right?
def requalts(current_state):
    if (current_state == CLOSURE_STATE):
        # Don't transition(?)
        next_state = CLOSURE_STATE
    else:
        # Check constraints
        # CONFIGURATION POINT
        if (len(preferences_not_set())>0):
            next_state = REQUEST_MISSING_PREFERENCES_STATE
        else:
            # Perform the lookup of restaurants in the db
            g_available_restaurants = find_possible_restaurants()
            # Check for availability
            if len(g_available_restaurants==0):
                next_state = INFORM_NO_MATCHES_STATE
            else:
                next_state = SUGGEST_RESTAURANT_STATE
    return next_state

def reqmore(current_state):
    if (current_state == WELCOME_STATE):
        # Don't transition(?)
        next_state = WELCOME_STATE
    elif (current_state == INFORM_NO_MATCHES_STATE):
        # Don't transition(?)
        next_state = INFORM_NO_MATCHES_STATE
    elif (current_state == REQUEST_MISSING_PREFERENCES_STATE):
        # Don't transition(?)
        next_state = REQUEST_MISSING_PREFERENCES_STATE
    elif (current_state == SUGGEST_RESTAURANT_STATE):
        #TODO
        next_state = SUGGEST_RESTAURANT_STATE
    elif (current_state == PROVIDE_DESCRIPTION_STATE):
        # Like suggest
        next_state = PROVIDE_DESCRIPTION_STATE
    elif (current_state == PROVIDE_DETAILS_STATE):
        # Like suggest
        next_state = PROVIDE_DETAILS_STATE
    elif (current_state == CLOSURE_STATE):
        next_state = CLOSURE_STATE
    else:
        print("Generic error message generated when transitioning states")
        next_state = CLOSURE_STATE
    return next_state

def request(current_state):
    if (current_state == WELCOME_STATE):
        # Don't transition
        next_state = WELCOME_STATE
    elif (current_state == INFORM_NO_MATCHES_STATE):
        # Don't transition(?)
        next_state = INFORM_NO_MATCHES_STATE
    elif (current_state == REQUEST_MISSING_PREFERENCES_STATE):
        # Don't transition(?) 
        next_state = REQUEST_MISSING_PREFERENCES_STATE
    elif (current_state == SUGGEST_RESTAURANT_STATE):
        next_state = PROVIDE_DETAILS_STATE
    elif (current_state == PROVIDE_DESCRIPTION_STATE):
        next_state = PROVIDE_DETAILS_STATE
    elif (current_state == PROVIDE_DETAILS_STATE):
        next_state = PROVIDE_DETAILS_STATE
    elif (current_state == CLOSURE_STATE):
        # Don't transition(?)
        next_state = CLOSURE_STATE
    else:
        print("Generic error message generated when transitioning states")
        next_state = CLOSURE_STATE
    return next_state

def restart(current_state):
    reset_preferences()
    dump_restaurants_list()
    next_state = WELCOME_STATE
    return next_state

def thankyou(current_state):
    if (current_state == WELCOME_STATE):
        # Don't transition
        next_state = WELCOME_STATE
    elif (current_state == INFORM_NO_MATCHES_STATE):
        # Don't transition
        next_state = INFORM_NO_MATCHES_STATE
    elif (current_state == REQUEST_MISSING_PREFERENCES_STATE):
        # Don't transition
        next_state = REQUEST_MISSING_PREFERENCES_STATE
    elif (current_state == SUGGEST_RESTAURANT_STATE):
        # Most likely a closure, they might know the place
        next_state = CLOSURE_STATE
    elif (current_state == PROVIDE_DESCRIPTION_STATE):
        # Most likely a closure, they might know the place
        next_state = CLOSURE_STATE
    elif (current_state == PROVIDE_DETAILS_STATE):
        # Most likely a closure, they might know the place
        next_state = CLOSURE_STATE
    elif (current_state == CLOSURE_STATE):
        # Obviously a closure
        next_state = CLOSURE_STATE
    else:
        print("Generic error message generated when transitioning states")
        next_state = CLOSURE_STATE
    return next_state
# Fallback for the handler when act is not correctly classified as a valid act
# Which in theory should never happen
def invalidact(current_state):
    print("Something went terribly wrong. We shouldn't have reached here!")
    next_state = CLOSURE_STATE # report bug
    return next_state

# User dialog acts
g_dialog_acts = {
        ACK_ACT:ack,
        AFFIRM_ACT:affirm,
        BYE_ACT:bye,
        CONFIRM_ACT:confirm,
        DENY_ACT:deny,
        HELLO_ACT:hello,
        INFORM_ACT:inform,
        NEGATE_ACT:negate,
        NULL_ACT:null,
        REPEAT_ACT:repeat,
        REQUALTS_ACT:requalts,
        REQMORE_ACT:reqmore,
        REQUEST_ACT:request,
        RESTART_ACT:restart,
        THANKYOU_ACT:thankyou
}
INFORMING_ACTS = [
        DENY_ACT,
        NEGATE_ACT,
        INFORM_ACT,
        REQUALTS_ACT
]

# User preferences
g_preferences = {
        "food_type":" ",
        "location":" ",
        "price_range":" "
}
# Flag that checks updates on preferences
g_updates = False
# Restaurants found according to the preferences received
g_available_restaurants = []
# Currently selected restaurant for suggestion and/or description
g_selected_restaurant = ""

# Find preferences missing user input
def preferences_not_set():
    not_set = []
    for parameter in g_preferences:
        if g_preferences[parameter] == "":
            not_set.extend(parameter)
    return not_set
# Restart preferences
def reset_preferences():
    global g_preferences
    dump_restaurants_list()
    g_preferences = {
        "food_type":"",
        "location":"",
        "price_range":""
    }
    return
# Overwrite a preference. 
# Input:
# preference: <str> preference retrieved from the inform act
# value: <str> value retrieved from the inform act
# Output: <bool> True if no problems, False if preference does not exist
def set_preference(preference, value):
    dump_restaurants_list()
    setting = False
    if preference in g_preferences:
        g_preferences[preference] = value
        setting = True
    else:
        setting = False
    return setting
    
# Reset the available restaurants array
def dump_restaurants_list():
    global g_available_restaurants, g_selected_restaurant
    g_available_restaurants = []
    g_selected_restaurant = ""
    return

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
# TODO
def invalidstate():
    return "invalid state"

# Dialog state nodes
g_system_states = {
        WELCOME_STATE:welcome, 
        INFORM_NO_MATCHES_STATE:inform_no_matches, 
#        change_preferences":change_preferences, 
        REQUEST_MISSING_PREFERENCES_STATE:request_missing_preferences, 
        SUGGEST_RESTAURANT_STATE:suggest_restaurant,
        PROVIDE_DESCRIPTION_STATE:provide_description,
        PROVIDE_DETAILS_STATE:provide_details,
        CLOSURE_STATE:closure
}

# Determine state transition and system utterance
# Input:
# current_state: <str> current dialog state
# current_input: <str> current user utterance
# Output:
# <str>: next dialog state
# <str>: next system utterance
def dialog_transition(current_state, current_input):
    global g_updates
    g_updates = False # Make sure we don't recycle values
    next_dialog_state = ""
    next_system_utterance = ""
    
    current_act = get_act(current_input)
    if current_act == INFORMING_ACTS: 
        g_updates = manage_info(current_input)
    next_dialog_state = next_state(current_state, current_act)
    next_system_utterance = generate_utterance(next_dialog_state)
    return next_dialog_state, next_system_utterance

# Extract possible information contained in the utterance and attempt to 
# update preferences
# Input:
# current_input: <str> current user utterance
def manage_info(current_input):
    extracted_info = extract_information(current_input)
    l_updates = False
    for preference in extracted_info:
        l_updates = l_updates and set_preference(preference, extracted_info[preference])
    return l_updates

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
# Output: dictionary with <preference,value> pairs for g_preferences
def extract_information(utterance):
    #TODO
    extracted = {}
    return extracted

# Lookup possible restaurants with the given contraints in the preferences
def find_possible_restaurants():
    restaurant = []
    with open('/Users/Asun/Desktop/restaurantinfo.csv') as csvfile:
        readcsv = csv.reader(csvfile, delimiter=',')

        for row in readcsv:
            if g_preferences["food_type"] in row or g_preferences["location"] in row or g_preferences["price_range"] in row:
                restaurant.append(row)
    return restaurant

# Decide what the next state should be based on current state and dialog act
# Input
# current_state: <str> current dialog state
# current_act: <str> dialog act extracted from the user input
# Output: <str> next dialog state
def next_state(current_state, current_act):
    next_state = ""
    handler = g_dialog_acts.get(current_act, INVALIDACT_ACT)
    # Refer to "Handlers for the different dialog acts"
    if handler == INVALIDACT_ACT:
        print("Something went terribly wrong. We shouldn't have reached here!")
        next_state = CLOSURE_STATE # report bug
    else:
        next_state = handler(current_act)
    return next_state

# Build the next utterance based on the current state of the dialog
# Input:
# state: <str> next dialog state
# Output: <str> next system utterance
def generate_utterance(current_state):
    utterance = ""
    handler = g_system_states.get(current_state, INVALIDSTATE_STATE)
    # Refer to "Handlers for the different dialog acts"
    if handler == INVALIDSTATE_STATE:
        print("Something went terribly wrong. We shouldn't have reached here!")
        utterance = "An error occurred. Report dialog log" # report bug
    else:
        utterance = handler()
    return utterance


# Start a dialog
def init_dialog():
    reset_preferences()
    print("Welcome to the restaurant selection assistant. Please enter your preferences.")
    current_state = WELCOME_STATE
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