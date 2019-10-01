from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
from keras.models import load_model
import json
from Levenshtein import distance
import operator
import csv

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
            if len(g_available_restaurants)==0 :
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
            if len(g_available_restaurants) ==0 :
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
        "food":" ",
        "area":" ",
        "price":" "
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
        "food":"",
        "area":"",
        "price":""
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
    if value == []:
        return setting
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
    return "Welcome to the restaurant selection assistant. Please enter your preferences."
# TODO
def inform_no_matches():
    if len(restaurants) == 0:
        no_matches = "There aren't restaurants matching those preferences"
    return no_matches
# Deleted, no point in having this dialog state
#def change_preferences():
#    return "change_preferences message"
# TODO
def request_missing_preferences():
    missing = []
    if g_preferences["food_type"] == " ":
        missing.append("food type")
    if g_preferences["location"] == " ":
        missing.append("location")
    if g_preferences["price_range"] == " ":
        missing.append("price range")
    if len(missing) == 2:
        request_preferences = "Please introduce your preferences for %s and %s" % (missing[0], missing[1])
    elif len(missing) == 3:
        request_preferences = "Please introduce your preferences for %s, %s and %s" % (
            missing[0], missing[1], missing[2])
    else:
        request_preferences = "Please introduce your preferences for %s" % (missing[0])

    return request_preferences
# TODO
def suggest_restaurant():
    ran_restaurant = random.randint(0, len(restaurants))
    selected_restaurant = restaurants[ran_restaurant]
    print(selected_restaurant)
    suggest = "%s is a %s restaurant in the %s of the city and the prices are in the %s range" % (
        selected_restaurant[0], selected_restaurant[3], selected_restaurant[2], selected_restaurant[1])

    return suggest, selected_restaurant
# TODO
def provide_description():
    description = []
    descriptionname = []

    for d in request_description:
        if d == "price rnage":
            description.append(selected_restaurant[1])
            descriptionname.append(d)
        if d == "location":
            description.append(selected_restaurant[2])
            descriptionname.append(d)
        if d == "food type":
            description.append(selected_restaurant[3])
            descriptionname.append(d)

    if len(description) == 2:
        descriptions = "The %s is %s and the %s is %s" % (
        descriptionname[0], description[0], descriptionname[1], description[1])
    elif len(description) == 3:
        descriptions = "The %s is %s, the %s is %s and the %s is %s" % (
            descriptionname[0], description[0], descriptionname[1], description[1], description[2], description[2])
    else:
        descriptions = "The %s is %s" % (descriptionname[0], description[0])
    return descriptions
# TODO
def provide_details(request_detail):
    detail = []
    detailname = []

    for d in request_detail:
        if d == "phone number":
            detail.append(selected_restaurant[4])
            detailname.append(d)
        if d == "address":
            detail.append(selected_restaurant[5])
            detailname.append(d)
        if d == "post code":
            detail.append(selected_restaurant[6])
            detailname.append(d)

    if len(detail) == 2:
        details = "The %s is %s and the %s is %s" % (detailname[0], detail[0], detailname[1], detail[1])
    elif len(detail) == 3:
        details = "The %s is %s, the %s is %s and the %s is %s" % (
        detailname[0], detail[0], detailname[1], detail[1], detail[2], detailname[2])
    else:
        details = "The %s is %s" % (detailname[0], detail[0])

    return details
# TODO
def closure():
    return "Good bye"
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

    if current_act in INFORMING_ACTS:
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
        l_updates = set_preference(preference, extracted_info[preference]) or l_updates
    return l_updates


def __prepareDataSet(fileName):
    """
    Load the dataset into labels and utterances.

    :param fileName:
    :return:
    """

    labels = []
    utterances = []

    with open(fileName) as f:
        lines = f.readlines()

    for line in lines:
        try:
            act = line[:line.index(" ")]
            utterance = line[line.index(" "):line.index("\n")]

            try:
                labels.append(act.strip())
                utterances.append(utterance.strip())

            except KeyError:
                pass

        except ValueError:
            pass

    return labels, utterances


def __loadTokenizerAndEncoder(fileName):

    y, x = __prepareDataSet(fileName)

    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(x)

    encoder = LabelEncoder()
    encoder.fit(y)

    return tokenizer, encoder


# Extract the dialog act from the user utterance
# Input: 
# utterance: current user utterance
# Output: <str> dialog act identified
def get_act(utterance):

    tokenizer, encoder = __loadTokenizerAndEncoder(g_trainFileName)
    act = g_model.predict(np.array(tokenizer.texts_to_matrix([utterance], mode='count')))

    return encoder.classes_[np.argmax(act[0])]

# Extract the relevant information from the current input
# Input:
# utterance: <str> current user utterance classified as inform
# Output: dictionary with <preference,value> pairs for g_preferences
def extract_information(utterance):

    ontology = json.loads(open(g_ontologyFile).read())

    food_list = ontology["informable"]["food"]
    pricerange_list = ontology["informable"]["pricerange"]
    area_list = ontology["informable"]["area"]

    words = utterance.split(" ")
    food_match = {}
    pricerange_match = {}
    area_match = {}
    threshold = 3
    for word in words:
        for food in food_list:
            temp_score = distance(word, food)
            if temp_score < threshold:
                food_match[food] = temp_score

        for pricerange in pricerange_list:
            temp_score = distance(word, pricerange)
            if temp_score < threshold:
                pricerange_match[pricerange] = temp_score

        for area in area_list:
            temp_score = distance(word, area)
            if temp_score < threshold:
                area_match[area] = temp_score

    food_match = sorted(food_match.items(), key=operator.itemgetter(1))
    pricerange_match = sorted(pricerange_match.items(), key=operator.itemgetter(1))
    area_match = sorted(area_match.items(), key=operator.itemgetter(1))

    extracted = {
        "food": [],
        "price": [],
        "area": []
    }
    for food in food_match:
        if food[1] > 0:
            break
        elif food[1] == 0:
            extracted["food"].append(food[0])
        else:
            g_distant["food"].append(food[0])

    for price in pricerange_match:
        if price[1] > 0:
            break
        elif price[1] == 0:
            extracted["price"].append(price[0])

    for area in area_match:
        if area[1] > 0:
            break
        elif area[1] == 0:
            extracted["area"].append(area[0])

    return extracted

# Lookup possible restaurants with the given contraints in the preferences
def find_possible_restaurants():
    restaurant = []
    with open('/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1c/restaurantinfo.csv') as csvfile:
        readcsv = csv.reader(csvfile, delimiter=',')

        for row in readcsv:
            if g_preferences["food"] in row or g_preferences["area"] in row or g_preferences["price"] in row:
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
        next_state = handler(current_state)
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

g_model = ""
g_trainFileName = ""
g_ontologyFile = ""
# maximum words to use as a dictionary
max_words = 1000

# Start a dialog
def init_dialog(modelFile, trainFile, ontologyFile):
    global g_model
    global g_trainFileName
    global g_ontologyFile
    reset_preferences()
    print("Welcome to the restaurant selection assistant. Please enter your preferences.")
    current_state = WELCOME_STATE
    next_state = ""
    next_system_utterance = ""
    g_model = load_model(modelFile)
    g_trainFileName = trainFile
    g_ontologyFile = ontologyFile
    try:
        while True:
            current_input = input()
            next_state, next_system_utterance = dialog_transition(current_state, current_input)
            current_state = next_state
            print(next_system_utterance)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":

    modelFile = '/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1b/model/dcnn_model.h5'
    trainFileName = '/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1b/dataset-txt/label_train_dialogs.txt'
    ontologyFile = '/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1c/ontology_dstc2.json'

    init_dialog(modelFile, trainFileName, ontologyFile)
