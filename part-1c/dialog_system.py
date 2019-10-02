from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
from Levenshtein import distance
import numpy as np
import json, csv, operator, random

class Dialog:
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
    INVALIDACT_ACT = "invalid_act"  # fall back dialog act in case something weird happens

    # Of which these are recognized as having some kind of information to store
    INFORMING_ACTS = [
        AFFIRM_ACT,
        NEGATE_ACT,
        INFORM_ACT,
        REQALTS_ACT
    ]

    # Dialog states
    WELCOME_STATE = "welcome"
    INFORM_NO_MATCHES_STATE = "inform_no_matches"

    #        change_preferences_state = change_preferences""
    REQUEST_MISSING_PREFERENCES_STATE = "request_missing_preferences"
    SUGGEST_RESTAURANT_STATE = "suggest_restaurant"
    PROVIDE_DESCRIPTION_STATE = "provide_description"
    PROVIDE_DETAILS_STATE = "provide_details"
    CLOSURE_STATE = "closure"
    INVALIDSTATE_STATE = "invalid_state"  # fall back dialog state in case something weird happens


    def __init__(self, config):

        self.g_model = load_model(config["modelFile"])
        self.g_tokenizer, self.g_encoder = self.loadTokenizerAndEncoder(config["trainFileName"])
        self.g_ontology = json.loads(open(config["ontologyFile"]).read())
        self.restaurantInfoFile = config['restaurantInfoFile']
        self.levenshteinEditDistance = config["levenshteinEditDistance"]
        self.lowerCase = config["lowerCase"]
        self.baseline = config["baseline"]

        # User preferences
        self.g_preferences = {
            self.FOOD: [],
            self.AREA: [],
            self.PRICERANGE: []
        }

        # User possible spelling mistakes
        self.g_distant = {
            self.FOOD: [],
            self.AREA: [],
            self.PRICERANGE: []
        }

        # Flag that checks updates on preferences
        self.g_updates = False

        # Restaurants found according to the preferences received
        self.g_available_restaurants = []

        # Currently selected restaurant for suggestion and/or description
        self.g_selected_restaurant = ""

        # Possible spelling mistake being questioned
        self.g_mistake = []

        # Preference being questioned for mistakes atm
        self.g_preference_at_stake = ""

        # <User dialog act, next_state determining function> dictionary
        self.DIALOG_ACTS = {
            self.ACK_ACT: self.ack,
            self.AFFIRM_ACT: self.affirm,
            self.BYE_ACT: self.bye,
            self.CONFIRM_ACT: self.confirm,
            self.DENY_ACT: self.deny,
            self.HELLO_ACT: self.hello,
            self.INFORM_ACT: self.inform,
            self.NEGATE_ACT: self.negate,
            self.NULL_ACT: self.null,
            self.REPEAT_ACT: self.repeat,
            self.REQALTS_ACT: self.reqalts,
            self.REQUEST_ACT: self.request,
            self.RESTART_ACT: self.restart,
            self.THANKYOU_ACT: self.thankyou
        }

        # <Dialog state, utterance generation function> dictionary
        self.g_system_states = {
            self.WELCOME_STATE: self.welcome,
            self.INFORM_NO_MATCHES_STATE: self.inform_no_matches,
            #        change_preferences":change_preferences,
            self.REQUEST_MISSING_PREFERENCES_STATE: self.request_missing_preferences,
            self.SUGGEST_RESTAURANT_STATE: self.suggest_restaurant,
            self.PROVIDE_DESCRIPTION_STATE: self.provide_description,
            self.PROVIDE_DETAILS_STATE: self.provide_details,
            self.CLOSURE_STATE: self.closure
        }

    # -*- coding: utf-8 -*-
    #############################################################
    #### NEXT STATE DETERMINING FUNCTIONS (FROM DIALOG ACTS) ####
    #############################################################
    # Handlers for the different dialog acts
    # Output: <str> next dialog state
    # TODO should we move at all with this act?
    def ack(self, current_state):
        if (current_state == self.WELCOME_STATE):
            # Don't transition
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            # Don't transition
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            # Don't transition
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            # Don't transition
            next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            # Don't transition
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.PROVIDE_DETAILS_STATE):
            # Don't transition
            next_state = self.PROVIDE_DETAILS_STATE
        elif (current_state == self.CLOSURE_STATE):
            # Don't transition
            next_state = self.CLOSURE_STATE
        else:
            print("Generic error message generated when transitioning states")
            next_state = self.CLOSURE_STATE
        return next_state


    # TODO should we move at all with this act?
    def affirm(self, current_state):
        if (current_state == self.WELCOME_STATE):
            # Don't transition
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            # Don't transition
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            # User is answering a question on possible mistakes
            self.set_preference(self.g_preference_at_stake, self.g_mistake)
            self.g_preference_at_stake = ""
            self.g_mistake = []
            # Could refactorize code below (same as in inform act)
            # Check constraints
            # CONFIGURATION POINT
            if (len(self.preferences_not_set()) > 0):
                next_state = self.REQUEST_MISSING_PREFERENCES_STATE
            else:
                # Perform the lookup of restaurants in the db
                self.g_available_restaurants = self.find_possible_restaurants(self.restaurantInfoFile)
                # Check for availability
                if len(self.g_available_restaurants) == 0:
                    next_state = self.INFORM_NO_MATCHES_STATE
                else:
                    next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            # Don't transition
            next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            # Don't transition
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.PROVIDE_DETAILS_STATE):
            # Don't transition
            next_state = self.PROVIDE_DETAILS_STATE
        elif (current_state == self.CLOSURE_STATE):
            # Don't transition
            next_state = self.CLOSURE_STATE
        else:
            print("Generic error message generated when transitioning states")
            next_state = self.CLOSURE_STATE
        return next_state


    def bye(self, current_state):
        next_state = self.CLOSURE_STATE
        return next_state


    def confirm(self, current_state):
        if (current_state == self.WELCOME_STATE):
            # Don't transition
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            # Don't transition
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            # Don't transition
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            # Query description of the restaurant
            next_state = PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            # Don't transition
            next_state = PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.PROVIDE_DETAILS_STATE):
            # Don't transition
            next_state = self.PROVIDE_DETAILS_STATE
        elif (current_state == self.CLOSURE_STATE):
            # Don't transition(?)
            next_state = self.CLOSURE_STATE
        else:
            print("Generic error message generated when transitioning states")
            next_state = self.CLOSURE_STATE
        return next_state


    # TODO
    def deny(self, current_state):
        if (current_state == self.WELCOME_STATE):
            # The program was opened by mistake, we take
            next_state = self.CLOSURE_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            # Don't transition
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            # Don't transition
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            # TODO
            # TODO Extract relevant information
            # TODO update preferences if no updates this is actually reqalts
            # Check preferences again and act accordingly
            if (len(self.preferences_not_set()) > 0):  # We could land here, not redundant
                next_state = self.REQUEST_MISSING_PREFERENCES_STATE
            else:
                # Perform the lookup of restaurants in the db
                self.g_available_restaurants = self.find_possible_restaurants()
                # Check for availability
                if len(self.g_available_restaurants) == 0:
                    next_state = self.INFORM_NO_MATCHES_STATE
                else:
                    next_state = self.SUGGEST_RESTAURANT_STATE
            next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            # TODO like SUGGEST_RESTAURANT_STATE?
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.PROVIDE_DETAILS_STATE):
            # TODO like SUGGEST_RESTAURANT_STATE?
            next_state = self.PROVIDE_DETAILS_STATE
        elif (current_state == self.CLOSURE_STATE):
            # Don't transition(?)
            next_state = self.CLOSURE_STATE
        else:
            print("Generic error message generated when transitioning states")
            next_state = self.CLOSURE_STATE
        return next_state


    def hello(self, current_state):
        # Don't transition ever(?)
        return current_state


    # After an inform act only no matches or suggest are possible states
    # Moreover, inform act can be input from any other state
    def inform(self, current_state):
        if (current_state == self.CLOSURE_STATE):
            # Don't transition(?)
            next_state = self.CLOSURE_STATE
        else:
            # Check constraints
            # CONFIGURATION POINT
            if (len(self.preferences_not_set()) > 0):
                next_state = self.REQUEST_MISSING_PREFERENCES_STATE
            else:
                # Perform the lookup of restaurants in the db
                self.g_available_restaurants = self.find_possible_restaurants(self.restaurantInfoFile)
                # Check for availability
                if len(self.g_available_restaurants) == 0:
                    next_state = self.INFORM_NO_MATCHES_STATE
                else:
                    next_state = self.SUGGEST_RESTAURANT_STATE
        return next_state


    # TODO
    def negate(self, current_state):
        if (current_state == self.WELCOME_STATE):
            # Don't transition(?)
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            # Don't transition(?)
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            # User is answering a question on possible mistakes
            g_mistake = []
            g_preference_at_stake = ""
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            # TODO This is actually reqalts
            next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            # TODO This is actually inform
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.PROVIDE_DETAILS_STATE):
            # TODO This is actually inform
            next_state = self.PROVIDE_DETAILS_STATE
        elif (current_state == self.CLOSURE_STATE):
            # Don't transition(?)
            next_state = self.CLOSURE_STATE
        else:
            print("Generic error message generated when transitioning states")
            next_state = self.CLOSURE_STATE
        return next_state


    # Don't transition ever, just repeat
    def null(self, current_state):
        return current_state


    # Don't transition ever, just repeat
    def repeat(self, current_state):
        return current_state


    # TODO like inform right?
    def reqalts(self, current_state):
        if (current_state == self.CLOSURE_STATE):
            # Don't transition(?)
            next_state = self.CLOSURE_STATE
        else:
            # Check constraints
            # CONFIGURATION POINT
            if (len(self.preferences_not_set()) > 0):
                next_state = self.REQUEST_MISSING_PREFERENCES_STATE
            else:
                # Check for availability
                if len(self.g_available_restaurants) == 0:
                    next_state = self.INFORM_NO_MATCHES_STATE
                else:
                    next_state = self.SUGGEST_RESTAURANT_STATE
        return next_state


    def reqmore(self, current_state):
        if (current_state == self.WELCOME_STATE):
            # Don't transition(?)
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            # Don't transition(?)
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            # Don't transition(?)
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            # TODO
            next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            # Like suggest
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.PROVIDE_DETAILS_STATE):
            # Like suggest
            next_state = self.PROVIDE_DETAILS_STATE
        elif (current_state == self.CLOSURE_STATE):
            next_state = self.CLOSURE_STATE
        else:
            print("Generic error message generated when transitioning states")
            next_state = self.CLOSURE_STATE
        return next_state


    def request(self, current_state):
        if (current_state == self.WELCOME_STATE):
            # Don't transition
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            # Don't transition(?)
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            # Don't transition(?)
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            next_state = self.PROVIDE_DETAILS_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            next_state = self.PROVIDE_DETAILS_STATE
        elif (current_state == self.PROVIDE_DETAILS_STATE):
            next_state = self.PROVIDE_DETAILS_STATE
        elif (current_state == self.CLOSURE_STATE):
            # Don't transition(?)
            next_state = self.CLOSURE_STATE
        else:
            print("Generic error message generated when transitioning states")
            next_state = self.CLOSURE_STATE
        return next_state


    def restart(self, current_state):
        self.reset_preferences()
        self.dump_restaurants_list()
        self.next_state = WELCOME_STATE
        return next_state


    def thankyou(self, current_state):
        if (current_state == self.WELCOME_STATE):
            # Don't transition
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            # Don't transition
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            # Don't transition
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            # Most likely a closure, they might know the place
            next_state = self.CLOSURE_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            # Most likely a closure, they might know the place
            next_state = self.CLOSURE_STATE
        elif (current_state == self.PROVIDE_DETAILS_STATE):
            # Most likely a closure, they might know the place
            next_state = self.CLOSURE_STATE
        elif (current_state == self.CLOSURE_STATE):
            # Obviously a closure
            next_state = self.CLOSURE_STATE
        else:
            print("Generic error message generated when transitioning states")
            next_state = self.CLOSURE_STATE
        return next_state


    # Fallback for the handler when act is not correctly classified as a valid act
    # Which in theory should never happen
    def invalidact(self, current_state):
        print("Something went terribly wrong. We shouldn't have found this unreachable act!")
        next_state = self.CLOSURE_STATE  # report bug
        return next_state


    ################################################
    #### SYSTEM UTTERANCES GENERATION FUNCTIONS ####
    ################################################
    # Dialog state nodes utterances generation handlers
    # Output: <str> next system utterance
    # TODO
    def welcome(self):
        return "Welcome to the restaurant selection assistant. Please enter your preferences."


    # TODO
    def inform_no_matches(self):
        if len(self.g_available_restaurants) == 0:
            no_matches = "There are no restaurants matching those preferences in my database."
        return no_matches


    # Deleted, no point in having this dialog state
    # def change_preferences():
    #    return "change_preferences message"
    # TODO
    def request_missing_preferences(self):
        missing = []
        # See what preferences are missing
        if not self.g_preferences[self.FOOD]:
            missing.append(self.FOOD)
        if not self.g_preferences[self.AREA]:
            missing.append(self.AREA)
        if not self.g_preferences[self.PRICERANGE]:
            missing.append(self.PRICERANGE)
        # Check if we have possible spelling mistakes
        if self.possible_mistakes():
            request_preferences = self.question_spelling_mistakes()
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
    def possible_mistakes(self):
        return len(self.g_distant[self.FOOD]) + len(self.g_distant[self.PRICERANGE]) + len(self.g_distant[self.AREA])


    # Create a question based on stored spelling mistakes, if there are any.
    # Output: <str> question if there are possible mistakes in g_distant, 0 otherwise
    def question_spelling_mistakes(self):
        question = 0
        # Check if we have possible misspellings
        question = self.spelling_mistakes(self.FOOD)
        if not question:  # Keep in mind that 0 evaluates to False
            question = self.spelling_mistakes(self.PRICERANGE)
            if not question:
                question = self.spelling_mistakes(self.AREA)
        return question


    # Spelling mistakes per preference (factorices code)
    # Input:
    # preference: <str> preference to check in g_distant
    # Output: <str> question if there are possible mistakes in g_distant[preference], 0 otherwise
    def spelling_mistakes(self, preference):
        # Make extra sure we are not recycling by any chance
        g_mistake = []
        g_preference_at_stake = ""

        question = 0
        if len(self.g_distant[preference]) > 0:
            mistakes = self.g_distant[preference][0]
            for value in self.g_distant[preference]:
                g_mistake.append(value)
                if mistakes == value:
                    continue  # This is only done for the pretty printing
                mistakes = mistakes + ', ' + value  # this pretty printing
            question = "I did not understand some of what you said. Did you mean %s %s?" % (mistakes, preference)
            g_preference_at_stake = preference
            self.g_distant[preference] = []
        return question


    # TODO
    def suggest_restaurant(self):
        if len(self.g_available_restaurants) == 0:
            suggest = "There are no restaurants left with those preferences"
        else:
            ran_restaurant = random.randint(1, len(g_available_restaurants)) - 1
            g_selected_restaurant = self.g_available_restaurants[ran_restaurant]
            self.g_available_restaurants.remove(g_selected_restaurant)
            suggest = "%s is a %s restaurant in the %s of the city and the prices are in the %s range" % (
                g_selected_restaurant[0], g_selected_restaurant[3], g_selected_restaurant[2], g_selected_restaurant[1])
            return suggest


    # TODO
    def provide_description(self):
        description = []
        descriptionname = []

        for d in request_description:
            if d == self.PRICERANGE:
                description.append(g_selected_restaurant[1])
                descriptionname.append(d)
            if d == self.AREA:
                description.append(g_selected_restaurant[2])
                descriptionname.append(d)
            if d == self.FOOD:
                description.append(g_selected_restaurant[3])
                descriptionname.append(d)
        if len(description) == 1:
            descriptions = "The %s is %s" % (descriptionname[0], description[0])
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
    def provide_details(self, request_detail):
        detail = []
        detailname = []

        for d in request_detail:
            if d == "phone number":
                detail.append(self.g_selected_restaurant[4])
                detailname.append(d)
            if d == "address":
                detail.append(self.g_selected_restaurant[5])
                detailname.append(d)
            if d == "post code":
                detail.append(self.g_selected_restaurant[6])
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


    def closure(self):
        return "Good bye"


    # Fallback for the handler when next_state is not correctly determined as a valid state
    # Which in theory should never happen
    def invalidstate(self):
        print("An error occurred, please report log")
        return "Something went terribly wrong. This is an unreachable dialog state!"

    #############################################
    #### PREFERENCES GLOBAL DICTIONARY 'API' ####
    #############################################
    # Find preferences missing user input
    # Output: <[str]> list of preferences not set
    def preferences_not_set(self):
        not_set = []
        for preference in self.g_preferences:
            if not self.g_preferences[preference]:
                not_set.extend(preference)
        return not_set


    # Restart preferences
    # Output: <bool> success resetting
    def reset_preferences(self):
        success = False
        self.dump_restaurants_list()
        self.g_preferences = {
            self.FOOD: [],
            self.AREA: [],
            self.PRICERANGE: []
        }
        self.g_updates = False
        success = True
        return success


    # Overwrite a preference.
    # Input:
    # preference: <str> preference retrieved from the inform act
    # value: <str> value retrieved from the inform act
    # Output: <bool> True if value updated, False otherwise
    def set_preference(self, preference, value):
        setting = False
        if not value:  # Skip preference, not present in current input
            return setting
        if preference in self.g_preferences and self.g_preferences[preference] != value:
            self.g_preferences[preference] = value
            setting = True
            self.dump_restaurants_list()
        else:
            setting = False
        return setting


    #######################################
    #### RESTAURANTS GLOBAL LIST 'API' ####
    #######################################
    # Reset the available restaurants array
    # Output: <bool> success resetting
    def dump_restaurants_list(self):
        success = False
        self.g_available_restaurants = []
        self.g_selected_restaurant = ""
        success = True
        return success


    # Lookup possible restaurants with the given contraints in the preferences
    # Output: <[str]> list of restaurants that match the preferences
    def find_possible_restaurants(self, restaurantInfoFile):
        restaurant = []
        with open(restaurantInfoFile) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')

            for row in readcsv:
                # TODO this is too flexible
                #            if g_preferences[FOOD][0] in row or g_preferences[AREA][0] in row or g_preferences[PRICERANGE][0] in row:
                if self.g_preferences[self.FOOD][0] in row and self.g_preferences[self.AREA][0] in row and self.g_preferences[self.PRICERANGE][0] in row:
                    restaurant.append(row)
        return restaurant


    ##########################################
    #### DIALOG TRANSITION CORE FUNCTIONS ####
    ##########################################
    # Start a dialog
    def init_dialog(self):
        # Preprare dialog assistant
        # 1. Make sure we don't recicle
        self.reset_preferences()
        next_state = ""

        # 2. Initialize dialog
        current_state = self.WELCOME_STATE  # Initial dialog state
        next_system_utterance = self.welcome()  # Initial system utterance
        print(next_system_utterance)
        try:
            while current_state != self.CLOSURE_STATE:
                current_input = input()
                if self.lowerCase == True:
                    current_input = current_input.lower()
                next_state, next_system_utterance = self.dialog_transition(current_state, current_input)
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
    def dialog_transition(self, current_state, current_input):
        self.g_updates = False  # Make sure we don't recycle
        next_dialog_state = ""
        next_system_utterance = ""

        current_act = self.get_act(current_input)

        if current_act in self.INFORMING_ACTS:
            self.g_updates = self.manage_info(current_input)
        next_dialog_state = self.next_state(current_state, current_act)
        next_system_utterance = self.generate_utterance(next_dialog_state)
        # This is a special case
        if current_act == self.REQALTS_ACT and next_dialog_state == self.INFORM_NO_MATCHES_STATE and not self.g_updates:
            next_system_utterance = "There are no more restaurants with those preferences. Enter new preferences"
            self.reset_preferences()
        return next_dialog_state, next_system_utterance


    # Extract the dialog act from the user utterance
    # Input:
    # utterance: current user utterance
    # Output: <str> dialog act identified
    def get_act(self, utterance):
        if self.baseline:
            act = self.keywordMatching(utterance)
            return act
        else:
            act = self.g_model.predict(np.array(self.g_tokenizer.texts_to_matrix([utterance], mode='count')))
            return self.g_encoder.classes_[np.argmax(act[0])]

    # Extract possible information contained in the utterance and attempt to
    # update preferences
    # Input:
    # current_input: <str> current user utterance
    def manage_info(self, current_input):
        extracted_info = self.extract_information(current_input)
        l_updates = False
        print(extracted_info)
        for preference in extracted_info:
            l_updates = self.set_preference(preference, extracted_info[preference]) or l_updates
        return l_updates

    # TODO this is too ugly to pass
    def aux(self, word, p_list, threshold, p_match):  # don't repeat code
        for elem in p_list:
            tmp_score = distance(word, elem)
            if tmp_score < threshold:
                p_match[elem] = tmp_score
        return p_match

    def aux2(self, p_match, preference, threshold, extracted, levenshteinEditDistance):  # don't repeat code
        flag = False
        for elem in p_match:
            # If we are sure of something we add it and discard anything else
            if elem[1] <= levenshteinEditDistance:
                extracted[preference].append(elem[0])
                flag = True
            # Reject anything above our threshold
            elif flag or elem[1] > threshold:
                break
            # Store separately possible spelling mistakes and await confirmation
            elif not flag:
                self.g_distant[preference].append(elem[0])
        return flag, extracted

    # Extract the relevant information from the current input
    # Input:
    # utterance: <str> current user utterance classified as inform
    # Output: dictionary with <preference,value> pairs for g_preferences
    def extract_information(self, utterance):
        food_list = self.g_ontology[self.INFORMABLE][self.FOOD]
        pricerange_list = self.g_ontology[self.INFORMABLE][self.PRICERANGE]
        area_list = self.g_ontology[self.INFORMABLE][self.AREA]

        words = utterance.split(" ")
        food_match = {}
        pricerange_match = {}
        area_match = {}
        threshold = 3

        for word in words:
            food_match = self.aux(word, food_list, threshold, food_match)
            pricerange_match = self.aux(word, pricerange_list, threshold, pricerange_match)
            area_match = self.aux(word, area_list, threshold, area_match)

        food_match = sorted(food_match.items(), key=operator.itemgetter(1))
        pricerange_match = sorted(pricerange_match.items(), key=operator.itemgetter(1))
        area_match = sorted(area_match.items(), key=operator.itemgetter(1))

        # Same structure as our g_preferences and g_distant
        extracted = {
            self.FOOD: [],
            self.PRICERANGE: [],
            self.AREA: []
        }

        food_found, extracted = self.aux2(food_match, self.FOOD, threshold, extracted, self.levenshteinEditDistance)
        pricerange_found, extracted = self.aux2(pricerange_match, self.PRICERANGE, threshold, extracted, self.levenshteinEditDistance)
        area_found, extracted = self.aux2(area_match, self.AREA, threshold, extracted, self.levenshteinEditDistance)

        return extracted


    # Decide what the next state should be based on current state and dialog act
    # Input
    # current_state: <str> current dialog state
    # current_act: <str> dialog act extracted from the user input
    # Output: <str> next dialog state
    def next_state(self, current_state, current_act):
        next_state = ""
        handler = self.DIALOG_ACTS.get(current_act, self.INVALIDACT_ACT)
        # Refer to "Handlers for the different dialog acts"
        next_state = handler(current_state)
        return next_state


    # Build the next utterance based on the current state of the dialog
    # Input:
    # state: <str> next dialog state
    # Output: <str> next system utterance
    def generate_utterance(self, current_state):
        utterance = ""
        handler = self.g_system_states.get(current_state, self.INVALIDSTATE_STATE)
        # Refer to "Handlers for the different dialog acts"
        utterance = handler()
        return utterance


    #######################################
    #### USER ACT IDENTIFICATION NEEDS ####
    #######################################
    # Both functions are copied from previous deliveries
    def prepareDataSet(self, fileName):
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


    def loadTokenizerAndEncoder(self, fileName):
        y, x = self.prepareDataSet(fileName)

        tokenizer = Tokenizer(num_words=self.MAX_WORDS)
        tokenizer.fit_on_texts(x)

        encoder = LabelEncoder()
        encoder.fit(y)

        return tokenizer, encoder

    def keywordMatching(self, utterance, repetition=False):

        dialog_acts = {}
        # Dialog acts keywords arrays
        ack_keywords = ["okay", "kay", "well", "great", "fine", "good", "thatll", "do"]
        affirm_keywords = ["yea", "yes", "correct", "right", "ye", "perfect", "yeah"]
        bye_keywords = ["goodbye", "bye"]
        confirm_keywords = ["is", "are", "they", "does",
                            "do"]  # always a question about the service (does it, do they, is it, are they). We omit 'it' for reasons
        deny_keywords = ["dont", "wrong", "no", "not", "change"]
        hello_keywords = ["hello", "hi", "halo"]
        negate_keywords = ["no"]
        null_keywords = []  # default to anything else
        repeat_keywords = ["repeat", "back", "again"]
        reqalts_keywords = ["another", "about", "else"]  # nonexistent in training data
        reqmore_keywords = ["more"]
        restart_keywords = ["start", "over", "reset", "restart"]
        thankyou_keywords = ["thanks", "thank"]
        # May be a question requesting (can i, may i, what is...)
        request_keywords = []
        request_details_keywords = ["much", "phone", "number", "postcode", "post", "code", "address", "type", "kind",
                                    "price", "range", "area", "telephone"]
        request_question_keywords = ["how", "whats", "what", "can", "may", "could", "need"]
        request_keywords.extend(request_details_keywords)
        request_keywords.extend(request_question_keywords)
        # We will need a special set of words for this set
        inform_food_type_keywords = ["thai", "chinese", "gastropub", "cuban", "seafood", "canapes", "indian", "african",
                                     "catalan", "turkish", "venetian", "porguguese", "oriental", "hungarian",
                                     "mediterranean", "creative", "asian", "traditional", "unusual", "malaysian",
                                     "jamaican", "french", "italian", "european", "american", "persian", "moroccan",
                                     "british", "korean", "romanian", "polish", "japanese", "english", "christmas",
                                     "barbecue", "cantonese", "spanish", "lebanese", "swedish", "mexican", "caribbean",
                                     "danish", "irish", "corsica", "afghan", "australian", "russian", "polynesian",
                                     "world", "kosher", "vegetarian", "tuscan", "scandinavian", "basque", "german",
                                     "persian", "eritrean", "austrian", "singaporean", "swiss", "scottish", "bistro",
                                     "welsh", "brazilian", "fusion", "steak", "pub", "halal", "gastro", "belgian",
                                     "steakhouse"]
        inform_price_range_keywords = ["cheap", "moderately", "moderate", "priced", "expensive"]
        inform_area_keywords = ["south", "north", "east", "west", "center", "anywhere"]

        inform_keywords = ["any", "kind", "food", "restaurant", "town", "part", "looking", "for", "dont", "care",
                           "doesnt", "matter"]
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

        utterance_matches = {}  # not really used but could be handy
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
        dialog_matches = [k for k, v in utterance_matches_len.items() if v == max_matches]

        return dialog_matches[0][:dialog_matches[0].index('_')]

##############
#### MAIN ####
##############
if __name__ == "__main__":

    config = {"modelFile": '/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1b/model/dcnn_model.h5',
              "trainFileName": '/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1b/dataset-txt/label_train_dialogs.txt',
              "ontologyFile": '/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1c/ontology_dstc2.json',
              "restaurantInfoFile": '/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1c/restaurantinfo.csv',
              'levenshteinEditDistance': 0,
              'lowerCase': True,
              'baseline': True}


    dialog = Dialog(config)
    dialog.init_dialog()
