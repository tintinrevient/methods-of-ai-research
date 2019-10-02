from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
from Levenshtein import distance
import numpy as np
import json, csv, operator, random

# -*- coding: utf-8 -*-
#############################################################
#### NEXT STATE DETERMINING FUNCTIONS (FROM DIALOG ACTS) ####
#############################################################
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
    global g_mistake, g_preference_at_stake
    if (current_state == WELCOME_STATE):
        # Don't transition
        next_state = WELCOME_STATE
    elif (current_state == INFORM_NO_MATCHES_STATE):
        # Don't transition
        next_state = INFORM_NO_MATCHES_STATE
    elif (current_state == REQUEST_MISSING_PREFERENCES_STATE):
        # User is answering a question on possible mistakes
        set_preference(g_preference_at_stake, g_mistake)
        g_preference_at_stake = ""
        g_mistake = []
        # Could refactorize code below (same as in inform act)
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
        # TODO update preferences if no updates this is actually reqalts
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
    global g_available_restaurants
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
            if len(g_available_restaurants) == 0 :
                next_state = INFORM_NO_MATCHES_STATE
            else:
                next_state = SUGGEST_RESTAURANT_STATE
    return next_state

# TODO
def negate(current_state):
    global g_mistake, g_preference_at_stake
    if (current_state == WELCOME_STATE):
        # Don't transition(?)
        next_state = WELCOME_STATE
    elif (current_state == INFORM_NO_MATCHES_STATE):
        # Don't transition(?)
        next_state = INFORM_NO_MATCHES_STATE
    elif (current_state == REQUEST_MISSING_PREFERENCES_STATE):
        # User is answering a question on possible mistakes
        g_mistake = []
        g_preference_at_stake = ""
        next_state = REQUEST_MISSING_PREFERENCES_STATE
    elif (current_state == SUGGEST_RESTAURANT_STATE):
        # TODO This is actually reqalts
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
def reqalts(current_state):
    global g_available_restaurants
    if (current_state == CLOSURE_STATE):
        # Don't transition(?)
        next_state = CLOSURE_STATE
    else:
        # Check constraints
        # CONFIGURATION POINT
        if (len(preferences_not_set())>0):
            next_state = REQUEST_MISSING_PREFERENCES_STATE
        else:
            # Check for availability
            if len(g_available_restaurants)==0:
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
    print("Something went terribly wrong. We shouldn't have found this unreachable act!")
    next_state = CLOSURE_STATE # report bug
    return next_state


################################################
#### SYSTEM UTTERANCES GENERATION FUNCTIONS ####
################################################
# Dialog state nodes utterances generation handlers
# Output: <str> next system utterance
#TODO
def welcome():
    return "Welcome to the restaurant selection assistant. Please enter your preferences."

# TODO
def inform_no_matches():
    if len(g_available_restaurants) == 0:
        no_matches = "There are no restaurants matching those preferences in my database."
    return no_matches

# Deleted, no point in having this dialog state
#def change_preferences():
#    return "change_preferences message"
# TODO
def request_missing_preferences():
    global g_mistake
    missing = []
    # See what preferences are missing
    if g_preferences[FOOD] == []:
        missing.append(FOOD)
    if g_preferences[AREA] == []:
        missing.append(AREA)
    if g_preferences[PRICERANGE] == []:
        missing.append(PRICERANGE)
    # Check if we have possible spelling mistakes
    if possible_mistakes():
        request_preferences = question_spelling_mistakes()
    # Else we just need to ask for missing preferences
    else:
        if len(missing) == 1:
            request_preferences = "Please introduce your preferences for %s" % (missing[0])
        elif len(missing) == 2:
            request_preferences = "Please introduce your preferences for %s and %s" % (missing[0], missing[1])
        elif len(missing) == 3:
            request_preferences = "Please introduce your preferences for %s, %s and %s" % (
                missing[0], missing[1], missing[2])
        else:
            request_preferences = "This preferences request shouldn't be possible :("

    return request_preferences

# Are there any possible spelling mistakes currently stored?
# Output: <int> number of possible mistakes committed
def possible_mistakes():
    return len(g_distant[FOOD]) + len(g_distant[PRICERANGE]) + len(g_distant[AREA])

# Create a question based on stored spelling mistakes, if there are any.
# Output: <str> question if there are possible mistakes in g_distant, 0 otherwise
def question_spelling_mistakes():
    question = 0
    # Check if we have possible misspellings
    question = spelling_mistakes(FOOD)
    if not question: # Keep in mind that 0 evaluates to False
        question = spelling_mistakes(PRICERANGE)
        if not question:
            question = spelling_mistakes(AREA)        
    return question

# Spelling mistakes per preference (factorices code)
# Input:
# preference: <str> preference to check in g_distant
# Output: <str> question if there are possible mistakes in g_distant[preference], 0 otherwise
def spelling_mistakes(preference):
    global g_mistake, g_preference_at_stake
    # Make extra sure we are not recycling by any chance
    g_mistake = []
    g_preference_at_stake = ""
    
    question = 0
    if len(g_distant[preference]) > 0:
        mistakes = g_distant[preference][0]
        for value in g_distant[preference]:
            g_mistake.append(value)
            if mistakes == value:
                continue # This is only done for the pretty printing
            mistakes = mistakes + ', ' + value # this pretty printing
        question = "I did not understand some of what you said. Did you mean %s %s?" % (mistakes, preference)
        g_preference_at_stake = preference
        g_distant[preference] = []
    return question
# TODO
def suggest_restaurant():
    global g_selected_restaurant
    if len(g_available_restaurants) == 0:
        suggest = "There are no restaurants left with those preferences"
    else:
        ran_restaurant = random.randint(1, len(g_available_restaurants)) - 1
        g_selected_restaurant = g_available_restaurants[ran_restaurant]
        g_available_restaurants.remove(g_selected_restaurant)
        suggest = "%s is a %s restaurant in the %s of the city and the prices are in the %s range" % (
            g_selected_restaurant[0], g_selected_restaurant[3], g_selected_restaurant[2], g_selected_restaurant[1])
        return suggest
    
# TODO
def provide_description():
    description = []
    descriptionname = []

    for d in request_description:
        if d == PRICERANGE:
            description.append(g_selected_restaurant[1])
            descriptionname.append(d)
        if d == AREA:
            description.append(g_selected_restaurant[2])
            descriptionname.append(d)
        if d == FOOD:
            description.append(g_selected_restaurant[3])
            descriptionname.append(d)
    if len(description) == 1:
        descriptions = "The %s is %s" %(descriptionname[0], description[0])
    elif len(description) == 2:
        descriptions = "The %s is %s and the %s is %s" % (
        descriptionname[0], description[0], descriptionname[1], description[1])
    elif len(description) == 3:
        descriptions = "The %s is %s, the %s is %s and the %s is %s" % (
            descriptionname[0], description[0], descriptionname[1], description[1], description[2], description[2])
    else:
        descriptions = "This description shouldn't be possible :("
    return descriptions

# TODO
def provide_details(request_detail):
    detail = []
    detailname = []

    for d in request_detail:
        if d == "phone number":
            detail.append(g_selected_restaurant[4])
            detailname.append(d)
        if d == "address":
            detail.append(g_selected_restaurant[5])
            detailname.append(d)
        if d == "post code":
            detail.append(g_selected_restaurant[6])
            detailname.append(d)
    if len(detail) == 1:
        details = "The %s is %s" % (detailname[0], detail[0])
    elif len(detail) == 2:
        details = "The %s is %s and the %s is %s" % (detailname[0], detail[0], detailname[1], detail[1])
    elif len(detail) == 3:
        details = "The %s is %s, the %s is %s and the %s is %s" % (
        detailname[0], detail[0], detailname[1], detail[1], detail[2], detailname[2])
    else:
        details = "This detail shouldn't be possible :("

    return details

def closure():
    return "Good bye"

# Fallback for the handler when next_state is not correctly determined as a valid state
# Which in theory should never happen
def invalidstate():
    print("An error occurred, please report log")
    return "Something went terribly wrong. This is an unreachable dialog state!"


############################
#### REUSABLE CONSTANTS ####
############################
# maximum words to use as a dictionary
MAX_WORDS = 1000

# Values used in common with the ontolgy.json files
REQUESTABLE = "requestable"
INFORMABLE = "informable"
FOOD = "food"
PRICERANGE = "pricerange"
AREA = "area"

# User recognizable dialog acts
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
REQALTS_ACT = "reqalts"
REQMORE_ACT = "reqmore"
REQUEST_ACT = "request"
RESTART_ACT = "restart"
THANKYOU_ACT = "thankyou"
INVALIDACT_ACT = "invalid_act" #fall back dialog act in case something weird happens

# Of which these are recognized as having some kind of information to store
INFORMING_ACTS = [
        AFFIRM_ACT,
        NEGATE_ACT,
        INFORM_ACT,
        REQALTS_ACT
]

# <User dialog act, next_state determining function> dictionary
DIALOG_ACTS = {
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
        REQALTS_ACT:reqalts,
        REQMORE_ACT:reqmore,
        REQUEST_ACT:request,
        RESTART_ACT:restart,
        THANKYOU_ACT:thankyou
}

# Dialog states
WELCOME_STATE = "welcome"
INFORM_NO_MATCHES_STATE = "inform_no_matches"

#        change_preferences_state = change_preferences""
REQUEST_MISSING_PREFERENCES_STATE = "request_missing_preferences"
SUGGEST_RESTAURANT_STATE = "suggest_restaurant"
PROVIDE_DESCRIPTION_STATE = "provide_description"
PROVIDE_DETAILS_STATE = "provide_details"
CLOSURE_STATE = "closure"
INVALIDSTATE_STATE = "invalid_state" #fall back dialog state in case something weird happens

# <Dialog state, utterance generation function> dictionary
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


##################################################
#### GLOBAL VARIABLES USED ACROSS THE PROGRAM ####
##################################################
# Model used to identify user acts
g_model = ""

# Ontology with relevant extracts of information on the db
g_ontology = ""

# User preferences
g_preferences = {
        FOOD:[],
        AREA:[],
        PRICERANGE:[]
}

# User possible spelling mistakes
g_distant = {
        FOOD: [],
        AREA: [],
        PRICERANGE: []
}

# Flag that checks updates on preferences
g_updates = False

# Restaurants found according to the preferences received
g_available_restaurants = []

# Currently selected restaurant for suggestion and/or description
g_selected_restaurant = ""

# Possible spelling mistake being questioned
g_mistake = []

# Preference being questioned for mistakes atm
g_preference_at_stake = ""

# Tokenizer, used in the finding of the user act
g_tokenizer = ""

# Encoder, used in the finidng of the user act
g_encoder = ""



#############################################
#### PREFERENCES GLOBAL DICTIONARY 'API' ####
#############################################
# Find preferences missing user input
# Output: <[str]> list of preferences not set
def preferences_not_set():
    not_set = []
    for preference in g_preferences:
        if not g_preferences[preference]:
            not_set.extend(preference)
    return not_set

# Restart preferences
# Output: <bool> success resetting
def reset_preferences():
    global g_preferences, g_updates
    success = False
    dump_restaurants_list()
    g_preferences = {
        FOOD: [],
        AREA: [],
        PRICERANGE: []
    }
    g_updates = False
    success = True
    return success

# Overwrite a preference. 
# Input:
# preference: <str> preference retrieved from the inform act
# value: <str> value retrieved from the inform act
# Output: <bool> True if value updated, False otherwise
def set_preference(preference, value):
    setting = False
    if value == []: # Skip preference, not present in current input 
        return setting
    if preference in g_preferences and g_preferences[preference] != value:
        g_preferences[preference] = value
        setting = True
        dump_restaurants_list()
    else:
        setting = False
    return setting


#######################################
#### RESTAURANTS GLOBAL LIST 'API' ####
#######################################
# Reset the available restaurants array
# Output: <bool> success resetting
def dump_restaurants_list():
    global g_available_restaurants, g_selected_restaurant
    success = False
    g_available_restaurants = []
    g_selected_restaurant = ""
    success = True
    return success

# Lookup possible restaurants with the given contraints in the preferences
# Output: <[str]> list of restaurants that match the preferences
def find_possible_restaurants():
    restaurant = []
    with open('/home/feilem/Documents/git/methods-of-ai-research/part-1c/restaurantinfo.csv') as csvfile:
        readcsv = csv.reader(csvfile, delimiter=',')

        for row in readcsv:
            # TODO this is too flexible
#            if g_preferences[FOOD][0] in row or g_preferences[AREA][0] in row or g_preferences[PRICERANGE][0] in row:
            if g_preferences[FOOD][0] in row and g_preferences[AREA][0] in row and g_preferences[PRICERANGE][0] in row:
                restaurant.append(row)
    return restaurant


##########################################
#### DIALOG TRANSITION CORE FUNCTIONS ####
##########################################
# Start a dialog
def init_dialog(modelFile, trainFile, ontologyFile):
    global g_model, g_ontology, g_encoder, g_tokenizer
    # Preprare dialog assistant
    # 1. Make sure we don't recicle
    reset_preferences() 
    next_state = ""
    # 2. Load tools
    g_model = load_model(modelFile)
    g_tokenizer, g_encoder = __loadTokenizerAndEncoder(trainFileName)
    g_ontology = json.loads(open(ontologyFile).read())
    # 3. Initialize dialog
    current_state = WELCOME_STATE # Initial dialog state
    next_system_utterance = welcome() # Initial system utterance
    print(next_system_utterance)
    try:
        while current_state != CLOSURE_STATE:
            current_input = input()
            next_state, next_system_utterance = dialog_transition(current_state, current_input)
            current_state = next_state
            print(next_system_utterance)

    except KeyboardInterrupt:
        pass
    return

# Determine state transition and system utterance
# Input:
# current_state: <str> current dialog state
# current_input: <str> current user utterance
# Output:
# <str>: next dialog state
# <str>: next system utterance
def dialog_transition(current_state, current_input):
    global g_updates
    g_updates = False # Make sure we don't recycle
    next_dialog_state = ""
    next_system_utterance = ""
    
    current_act = get_act(current_input)

    if current_act in INFORMING_ACTS:
        g_updates = manage_info(current_input)
    next_dialog_state = next_state(current_state, current_act)
    next_system_utterance = generate_utterance(next_dialog_state)
    # This is a special case
    if current_act == REQALTS_ACT and next_dialog_state == INFORM_NO_MATCHES_STATE:
        next_system_utterance = "There are no more restaurants with those preferences. Enter new preferences"
        reset_preferences()
    return next_dialog_state, next_system_utterance

# Extract the dialog act from the user utterance
# Input: 
# utterance: current user utterance
# Output: <str> dialog act identified
def get_act(utterance):
    act = g_model.predict(np.array(g_tokenizer.texts_to_matrix([utterance], mode='count')))
    return g_encoder.classes_[np.argmax(act[0])]

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


# Extract the relevant information from the current input
# Input:
# utterance: <str> current user utterance classified as inform
# Output: dictionary with <preference,value> pairs for g_preferences
def extract_information(utterance):
    food_list = g_ontology[INFORMABLE][FOOD]
    pricerange_list = g_ontology[INFORMABLE][PRICERANGE]
    area_list = g_ontology[INFORMABLE][AREA]

    words = utterance.split(" ")
    food_match = {}
    pricerange_match = {}
    area_match = {}
    threshold = 3
    #TODO this is too ugly to pass
    def aux(word, p_list, threshold, p_match):
        for elem in p_list:
            tmp_score = distance(word, elem)
            if tmp_score < threshold:
                p_match[elem] = tmp_score
        return p_match
    for word in words:
        food_match = aux(word, food_list, threshold, food_match)
#        for food in food_list:
#            temp_score = distance(word, food)
#            if temp_score < threshold:
#                food_match[food] = temp_score
        pricerange_match = aux(word, pricerange_list, threshold, pricerange_match)
#        for pricerange in pricerange_list:
#            temp_score = distance(word, pricerange)
#            if temp_score < threshold:
#                pricerange_match[pricerange] = temp_score
        area_match = aux(word, area_list, threshold, area_match)
#        for area in area_list:
#            temp_score = distance(word, area)
#            if temp_score < threshold:
#                area_match[area] = temp_score

    food_match = sorted(food_match.items(), key=operator.itemgetter(1))
    pricerange_match = sorted(pricerange_match.items(), key=operator.itemgetter(1))
    area_match = sorted(area_match.items(), key=operator.itemgetter(1))

    # Same structure as our g_preferences and g_distant
    extracted = {
        FOOD: [],
        PRICERANGE: [],
        AREA: []
    }
    food_found = False # This flag will save us time
    for food in food_match:
        # If we are sure of something we add it and discard anything else
        if food[1] == 0:
            extracted[FOOD].append(food[0])
            food_found = True
        # Reject anything above our threshold
        elif food_found or food[1] > threshold:
            break
        # Store separately possible spelling mistakes and await confirmation
        elif not food_found:
            g_distant[FOOD].append(food[0]) 
    pricerange_found = False
    for price in pricerange_match:
        if price[1] == 0:
            extracted[PRICERANGE].append(price[0])
            pricerange_found = True
        elif pricerange_found or price[1] > threshold:
            break
        elif not pricerange_found:
            g_distant[PRICERANGE].append(price[0]) 
            
    area_found = False
    for area in area_match:
        if area[1] == 0:
            extracted[AREA].append(area[0])
            area_found = True
        elif area_found or area[1] > threshold:
            break
        elif not area_found:
            g_distant[AREA].append(area[0])

    return extracted

# Decide what the next state should be based on current state and dialog act
# Input
# current_state: <str> current dialog state
# current_act: <str> dialog act extracted from the user input
# Output: <str> next dialog state
def next_state(current_state, current_act):
    next_state = ""
    handler = DIALOG_ACTS.get(current_act, INVALIDACT_ACT)
    # Refer to "Handlers for the different dialog acts"
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
    utterance = handler()
    return utterance


#######################################
#### USER ACT IDENTIFICATION NEEDS ####
#######################################
# Both functions are copied from previous deliveries
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

    tokenizer = Tokenizer(num_words=MAX_WORDS)
    tokenizer.fit_on_texts(x)

    encoder = LabelEncoder()
    encoder.fit(y)

    return tokenizer, encoder


##############
#### MAIN ####
##############
if __name__ == "__main__":

    modelFile = '/home/feilem/Documents/git/methods-of-ai-research/part-1b/model/dcnn_model.h5'
    trainFileName = '/home/feilem/Documents/git/methods-of-ai-research/part-1b/dataset-txt/label_train_dialogs.txt'
    ontologyFile = '/home/feilem/Documents/git/methods-of-ai-research/part-1c/ontology_dstc2.json'
    
    init_dialog(modelFile, trainFileName, ontologyFile)