from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
from Levenshtein import distance
import numpy as np
import json, csv, operator, random, re


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
    REQUEST_MISSING_PREFERENCES_STATE = "request_missing_preferences"
    SUGGEST_RESTAURANT_STATE = "suggest_restaurant"
    PROVIDE_DESCRIPTION_STATE = "provide_description"
    CLOSURE_STATE = "closure"
    INVALIDSTATE_STATE = "invalid_state"  # fall back dialog state in case something weird happens

    # Details expressions
    PHONENUMBER = "phonenumber"
    ADDRESS = "address"
    POSTCODE = "postcode"
    DETAILS_EXPRESSIONS = {
        PHONENUMBER: ["telephone", "phone", "number", "contact"],
        ADDRESS: ["location", "direction", "directions", "where"],
        POSTCODE: ["post", "post-code"]
    }

    # Patterns for pattern matching
    PATTERNS_INFORM = [
        r"[I|i]'m looking for ([\w+\s]+)food",
        r"[I|i] want a restaurant that serves ([\w+\s]+)[food]?",
        r"[I|i] want a restaurant serving ([\w+\s]+)[food]?",
        r"[I|i]'m looking for a restaurant in the (\w+)",
        r"[I|i] would like a[n]? ([\w+\s]+)restaurant in the (\w+) [part]? of town",
        r"[I|i]'m looking for a[n]? (\w+) [priced]? restaurant in the (\w+) [part]? of town",
        r"[I|i]'m looking for a restaurant in (\w)+ [area|part]? that serves ([\w+\s]+)[food]?",
        r"[C|c]an [I|i] have a[n]? ([\w+\s]+)restaurant",
        r"[I|i]'m looking for a[n]? ([\w+\s]+)restaurant and it should serve ([\w+\s]+)food",
        r"[I|i] need a[n]? ([\w+\s]+)restaurant that is (\w+) priced",
        r"[I|i]'m looking for a[n]? (\w+) priced restaurant with (\w+) food",
        r"[W|w]hat is a[n]? ([\w+\s]+)restaurant in the (\w+) [part|area] of town",
        r"[W|w]hat about (\w+) food",
        r"[I|i] wanna find a[n]? (\w+) restaurant",
        r"[I|i]'m looking for ([\w+\s]+)food please",
        r"[F|f]ind a[n]? ([\w+\s]+)restaurant in the (\w+)"
    ]
    # Compilations of the patterns above
    PATTERNS_INFORM_COMPILED = []
    for i in range(len(PATTERNS_INFORM)):
        PATTERNS_INFORM_COMPILED.append(re.compile(PATTERNS_INFORM[i]))

    def __init__(self, config):
        # Load configuration
        self.g_model = load_model(config["modelFile"])
        self.g_tokenizer, self.g_encoder = self.loadTokenizerAndEncoder(config["trainFileName"])
        self.g_ontology = json.loads(open(config["ontologyFile"]).read())
        self.restaurantInfoFile = config['restaurantInfoFile']
        self.levenshteinEditDistance = config["levenshteinEditDistance"]
        self.lowerCase = config["lowerCase"]
        self.baseline = config["baseline"]
        self.outputAllCaps = config["outputAllCaps"]
        
        # Keyword matching baseline model
        self.baseline_model = {}

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

        # {<User dialog act, next_state determining function>} dictionary
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

        # {<Dialog state, utterance generation function>} dictionary
        self.g_system_states = {
            self.WELCOME_STATE: self.welcome,
            self.INFORM_NO_MATCHES_STATE: self.inform_no_matches,
            self.REQUEST_MISSING_PREFERENCES_STATE: self.request_missing_preferences,
            self.SUGGEST_RESTAURANT_STATE: self.suggest_restaurant,
            self.PROVIDE_DESCRIPTION_STATE: self.provide_description,
            self.CLOSURE_STATE: self.closure
        }

    # -*- coding: utf-8 -*-
    #############################################################
    #### NEXT STATE DETERMINING FUNCTIONS (FROM DIALOG ACTS) ####
    #############################################################
    # Handlers for the different dialog acts
    # Input:
    # current_state: <str> current dialog state
    # Output: <str> next dialog state
    
    # TODO should we move at all with this act?
    def ack(self, current_state):
        if (current_state == self.WELCOME_STATE):
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.CLOSURE_STATE):
            next_state = self.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self.system_print(sentence)
            next_state = self.CLOSURE_STATE
        return next_state

    # TODO
    def affirm(self, current_state):
        if (current_state == self.WELCOME_STATE):
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
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
                self.g_available_restaurants = self.find_possible_restaurants()
                # Check for availability
                if len(self.g_available_restaurants) == 0:
                    next_state = self.INFORM_NO_MATCHES_STATE
                else:
                    next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.CLOSURE_STATE):
            next_state = self.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self.system_print(sentence)
            next_state = self.CLOSURE_STATE
        return next_state

    def bye(self, current_state):
        next_state = self.CLOSURE_STATE
        return next_state

    def confirm(self, current_state):
        if (current_state == self.WELCOME_STATE):
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.CLOSURE_STATE):
            next_state = self.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self.system_print(sentence)
            next_state = self.CLOSURE_STATE
        return next_state

    # TODO
    def deny(self, current_state):
        if (current_state == self.WELCOME_STATE):
            # The program was opened by mistake, we take
            next_state = self.CLOSURE_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
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
        elif (current_state == self.CLOSURE_STATE):
            next_state = self.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self.system_print(sentence)
            next_state = self.CLOSURE_STATE
        return next_state

    def hello(self, current_state):
        return current_state

    # After an inform act only no matches or suggest are possible states
    # Moreover, inform act can be input from any other state
    def inform(self, current_state):
        if (current_state == self.CLOSURE_STATE):
            next_state = self.CLOSURE_STATE
        else:
            # Check constraints
            # CONFIGURATION POINT
            if (len(self.preferences_not_set()) > 0):
                next_state = self.REQUEST_MISSING_PREFERENCES_STATE
            else:
                # Perform the lookup of restaurants in the db
                self.g_available_restaurants = self.find_possible_restaurants()
                # Check for availability
                if len(self.g_available_restaurants) == 0:
                    next_state = self.INFORM_NO_MATCHES_STATE
                else:
                    next_state = self.SUGGEST_RESTAURANT_STATE
        return next_state

    # TODO
    def negate(self, current_state):
        if (current_state == self.WELCOME_STATE):
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            # User is answering a question on possible mistakes
            self.g_mistake = []
            self.g_preference_at_stake = ""
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            # This is actually reqalts
            next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            # This is actually inform
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.CLOSURE_STATE):
            next_state = self.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self.system_print(sentence)
            next_state = self.CLOSURE_STATE
        return next_state

    def null(self, current_state):
        return current_state

    def repeat(self, current_state):
        return current_state

    # TODO
    def reqalts(self, current_state):
        if (current_state == self.CLOSURE_STATE):
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
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            next_state = self.SUGGEST_RESTAURANT_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.CLOSURE_STATE):
            next_state = self.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self.system_print(sentence)
            next_state = self.CLOSURE_STATE
        return next_state

    def request(self, current_state):
        if (current_state == self.WELCOME_STATE):
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            next_state = self.PROVIDE_DESCRIPTION_STATE
        elif (current_state == self.CLOSURE_STATE):
            next_state = self.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self.system_print(sentence)
            next_state = self.CLOSURE_STATE
        return next_state

    def restart(self, current_state):
        self.reset_preferences()
        self.dump_restaurants_list()
        next_state = self.WELCOME_STATE
        return next_state

    def thankyou(self, current_state):
        if (current_state == self.WELCOME_STATE):
            next_state = self.WELCOME_STATE
        elif (current_state == self.INFORM_NO_MATCHES_STATE):
            next_state = self.INFORM_NO_MATCHES_STATE
        elif (current_state == self.REQUEST_MISSING_PREFERENCES_STATE):
            next_state = self.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == self.SUGGEST_RESTAURANT_STATE):
            next_state = self.CLOSURE_STATE
        elif (current_state == self.PROVIDE_DESCRIPTION_STATE):
            next_state = self.CLOSURE_STATE
        elif (current_state == self.CLOSURE_STATE):
            next_state = self.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self.system_print(sentence)
            next_state = self.CLOSURE_STATE
        return next_state

    # Fallback for the handler when act is not correctly classified as a valid act
    # Which in theory should never happen
    def invalidact(self, current_state):
        sentence = "Something went terribly wrong. We shouldn't have found this unreachable act!"
        self.system_print(sentence)
        next_state = self.CLOSURE_STATE
        return next_state

    ################################################
    #### SYSTEM UTTERANCES GENERATION FUNCTIONS ####
    ################################################
    # Dialog state nodes utterances generation handlers
    # Input:
    # utterance: <str> current user input
    # Output: <str> next system utterance
    
    def welcome(self, utterance):
        return "Welcome to the restaurant selection assistant. Please enter your preferences."

    def inform_no_matches(self, utterance):
        if len(self.g_available_restaurants) == 0:
            no_matches = "There are no %s restaurants in the %s price range located in the %s." % (
            self.g_preferences[self.FOOD], self.g_preferences[self.PRICERANGE], self.g_preferences[self.AREA])
        return no_matches

    def request_missing_preferences(self, utterance):
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

    def question_spelling_mistakes(self):
        """
        Create a question based on stored spelling mistakes, if there are any.
        Output: <str> question if there are possible mistakes in g_distant, 0 otherwise
        """
        # Check if we have possible misspellings
        question = self.spelling_mistakes(self.FOOD)
        if not question:  # Keep in mind that 0 evaluates to False
            question = self.spelling_mistakes(self.PRICERANGE)
            if not question:
                question = self.spelling_mistakes(self.AREA)
        return question

    def spelling_mistakes(self, preference):
        """
        Spelling mistakes per preference
        Input:
        preference: <str> preference to check in g_distant
        Output: <str> question if there are possible mistakes in g_distant[preference], 0 otherwise
        """
        # Make extra sure we are not recycling by any chance
        self.g_mistake = []
        self.g_preference_at_stake = ""

        question = 0
        if len(self.g_distant[preference]) > 0:
            mistakes = self.g_distant[preference][0]
            for value in self.g_distant[preference]:
                self.g_mistake.append(value)
                if mistakes == value:
                    continue  # This is only done for the pretty printing
                mistakes = mistakes + ', ' + value  # this pretty printing

            question = "I did not understand some of what you said. Did you mean %s %s?" % (mistakes, preference)

            self.g_preference_at_stake = preference
            self.g_distant[preference] = []
        return question

    def suggest_restaurant(self, utterance):
        if len(self.g_available_restaurants) == 0:
            suggest = "There are no restaurants left with those preferences"
        else:
            ran_restaurant = random.randint(1, len(self.g_available_restaurants)) - 1
            self.g_selected_restaurant = self.g_available_restaurants[ran_restaurant]
            self.g_available_restaurants.remove(self.g_selected_restaurant)
            suggest = "%s is a %s restaurant in the %s of the city and the prices are in the %s range" % (
                self.g_selected_restaurant[0], self.g_selected_restaurant[3], self.g_selected_restaurant[2],
                self.g_selected_restaurant[1])
        return suggest

    def provide_description(self, utterance):
        description = []
        descriptionname = []
        request_description = utterance.split(" ")
        # Check for description requests in current input
        for d in request_description:
            if self.check_description_elements(d, self.PRICERANGE):
                description.append(self.g_selected_restaurant[1])
                descriptionname.append(self.PRICERANGE)
            if self.check_description_elements(d, self.AREA):
                description.append(self.g_selected_restaurant[2])
                descriptionname.append(self.AREA)
            if self.check_description_elements(d, self.FOOD):
                description.append(self.g_selected_restaurant[3])
                descriptionname.append(self.FOOD)
            if self.check_details_elements(d, self.PHONENUMBER):
                description.append(self.g_selected_restaurant[4])
                descriptionname.append(self.PHONENUMBER)
            if self.check_details_elements(d, self.ADDRESS):
                description.append(self.g_selected_restaurant[5])
                descriptionname.append(self.ADDRESS)
            if self.check_details_elements(d, self.POSTCODE):
                description.append(self.g_selected_restaurant[6])
                descriptionname.append(self.POSTCODE)
        requests = len(description)
        if requests > 0:
            descriptions = "The "
            for i in range(requests):
                if i > 0:
                    if i == requests:
                        descriptions = descriptions + " and "
                    else:
                        descriptions = descriptions + ", the "
                descriptions = descriptions + ("%s is %s" % (descriptionname[i], description[i]))
        # The description requests were not clear
        else:
            descriptions = "What do you want to know about the restaurant? (food, area, pricerange, contact information, post code, address)"  # "This description is triggered if there is any misspeling on keywords

        return descriptions

    def check_description_elements(self, word, ontology_subset):
        """    
        Check if a word matches a certain ontology subset
        Input:
        word: <str> word to check
        ontology_subset: <str> [AREA | PRICERANGE | FOOD]
        Output: <bool> True if it matches, False otherwise
        """
        checks_out = word == ontology_subset or word in self.g_ontology[self.INFORMABLE][ontology_subset]
        return checks_out

    def check_details_elements(self, word, details_subset):
        """
        Check if a word matches a certain details expressions subset
        Input:
        word: <str> word to check
        ontology_subset: <str> [PHONENUMBER | POSTCODE | ADDRESS]
        Output: <bool> True if it matches, False otherwise
        """
        checks_out = word == details_subset or word in self.DETAILS_EXPRESSIONS[details_subset]
        return checks_out


    def closure(self, utterance):
        sentence = "Good bye"
        return sentence

    # Fallback for the handler when next_state is not correctly determined as a valid state
    # Which in theory should never happen
    def invalidstate(self, utterance):
        sentence = "An error occurred, please report log"
        result = "Something went terribly wrong. This is an unreachable dialog state!"
        self.system_print(sentence.upper())
        return result

    #############################################
    #### PREFERENCES GLOBAL DICTIONARY 'API' ####
    #############################################
    def preferences_not_set(self):
        """
        Find preferences missing user input
        Output: <[str]> list of preferences not set
        """
        not_set = []
        for preference in self.g_preferences:
            if not self.g_preferences[preference]:
                not_set.extend(preference)
        return not_set

    def reset_preferences(self):
        """
        Restart preferences
        Output: <bool> success resetting
        """
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

    def set_preference(self, preference, value):
        """
        Overwrite a preference.
        Input:
        preference: <str> preference retrieved from the inform act
        value: <[str]> list of values retrieved from the inform act
        Output: <bool> True if value updated, False otherwise
        """
        setting = False
        if not value:  # Skip preference, not present in current input (empty list)
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
    def dump_restaurants_list(self):
        """
        Reset the available restaurants array
        Output: <bool> success resetting
        """
        success = False
        self.g_available_restaurants = []
        self.g_selected_restaurant = ""
        success = True
        return success

    def find_possible_restaurants(self):
        """
        Lookup possible restaurants with the given contraints in the preferences
        Output: <[str]> list of restaurants that match the preferences
        """
        restaurant = []
        with open(self.restaurantInfoFile) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')

            for row in readcsv:
                # TODO
                if self.g_preferences[self.FOOD][0] in row and self.g_preferences[self.AREA][0] in row and \
                                self.g_preferences[self.PRICERANGE][0] in row:
                    restaurant.append(row)
        return restaurant

    ##########################################
    #### DIALOG TRANSITION CORE FUNCTIONS ####
    ##########################################
    def init_dialog(self):
        """
        Start a dialog
        """
        # Preprare dialog assistant
        # 1. Make sure we don't recicle
        self.reset_preferences()
        next_state = ""
        next_system_utterance = ""
        if self.baseline:
            self.baseline_model = self.__initModel()

        # 2. Initialize dialog
        current_state = self.WELCOME_STATE  # Initial dialog state
        next_system_utterance = self.welcome("")  # Initial system utterance
        self.system_print(next_system_utterance)
        try:
            while current_state != self.CLOSURE_STATE:
                current_input = input()
                if self.lowerCase == True:
                    current_input = current_input.lower()
                next_state, next_system_utterance = self.dialog_transition(current_state, current_input)
                current_state = next_state
                self.system_print(next_system_utterance)

        except KeyboardInterrupt:
            pass
        return
    
    def system_print(self, utterance):
        """
        System printing handler
        Input:
        utterance: <str> current system utterance to be printed
        """
        if self.outputAllCaps:
            print(utterance.upper())
        else:
            print(utterance)
        return

    def dialog_transition(self, current_state, current_input):
        """
        Determine state transition and system utterance
        Input:
        current_state: <str> current dialog state
        current_input: <str> current user utterance
        Output:
        <str>: next dialog state
        <str>: next system utterance
        """
        # Make sure we don't recycle
        self.g_updates = False  
        next_dialog_state = ""
        next_system_utterance = ""

        current_act = self.get_act(current_input)
        if current_act in self.INFORMING_ACTS:
            self.g_updates = self.manage_info(current_input)
        next_dialog_state = self.next_state(current_state, current_act)
        next_system_utterance = self.generate_utterance(next_dialog_state, current_input)
        
        # Next is a special case
        if current_act == self.REQALTS_ACT and next_dialog_state == self.INFORM_NO_MATCHES_STATE and not self.g_updates:
            next_system_utterance = "There are no more %s restaurants in the %s price range in the %s of the city. Resetting preferences. Please enter new ones." % (
            self.g_preferences[self.FOOD], self.g_preferences[self.PRICERANGE], self.g_preferences[self.AREA])
            self.reset_preferences()

        return next_dialog_state, next_system_utterance

    def get_act(self, utterance):
        """
        Extract the dialog act from the user utterance
        Input:
        utterance: <str> current user utterance
        Output: <str> dialog act identified
        """
        if (self.baseline):
            act = self.keywordMatching(utterance)
            return act
        else:
            act = self.g_model.predict(np.array(self.g_tokenizer.texts_to_matrix([utterance], mode='count')))
            return self.g_encoder.classes_[np.argmax(act[0])]

    def manage_info(self, current_input):
        """
        Extract possible information contained in the utterance and attempt to
        update preferences
        Input:
        current_input: <str> current user utterance
        Output: <bool> True if a preference was updated, False otherwise
        """
        extracted_info = self.extract_information(current_input)
        l_updates = False
        for preference in extracted_info:
            l_updates = self.set_preference(preference, extracted_info[preference]) or l_updates
        return l_updates

    def extract_information(self, utterance):
        """
        Extract the relevant information from the current input
        Input:
        utterance: <str> current user utterance classified as inform
        Output: dictionary with <preference,value> pairs for g_preferences
        """
        food_list = self.g_ontology[self.INFORMABLE][self.FOOD]
        pricerange_list = self.g_ontology[self.INFORMABLE][self.PRICERANGE]
        area_list = self.g_ontology[self.INFORMABLE][self.AREA]

        words = utterance.split(" ") # TODO pattern-matching
        
        # <word, score> dictionaries
        food_match = {}
        pricerange_match = {}
        area_match = {}
        # Maximum value a word can score to enter the dictionaries above
        threshold = 3 #TODO
        
        # AUX: Extract the relevant information from the current input, focusing on a single preference
        # Input:
        # word: <str> word to evaluate
        # p_list: <[str]> list of keywords for a preference
        # threshold: <int> maximum value a word can score to enter the preferences dictionaries
        # p_match: <word, score> preferences dictionary
        # Output: p_match updated with valid word entries
        def extract_preference_info(word, p_list, threshold, p_match):
            for elem in p_list:
                tmp_score = distance(word, elem)
                if tmp_score < threshold:
                    p_match[elem] = tmp_score
            return p_match

        for word in words:
            food_match = extract_preference_info(word, food_list, threshold, food_match)
            pricerange_match = extract_preference_info(word, pricerange_list, threshold, pricerange_match)
            area_match = extract_preference_info(word, area_list, threshold, area_match)

        food_match = sorted(food_match.items(), key=operator.itemgetter(1))
        pricerange_match = sorted(pricerange_match.items(), key=operator.itemgetter(1))
        area_match = sorted(area_match.items(), key=operator.itemgetter(1))

        # Same structure as our g_preferences and g_distant
        extracted = {
            self.FOOD: [],
            self.PRICERANGE: [],
            self.AREA: []
        }
        
        # AUX: Select extracted preferences according to their edit distances 
        # Input: 
        # p_match: <word, score> dictionary for a preference
        # preference: <str> preference 
        # threshold: <int> maxiumum score to consider
        # extraced: <preference, [str]> dictionary of extracted preferences
        # Output: 
        # flag: <bool> True if any preferences found for this preference, False otherwise
        # extracted: <preference, [str]> dictionary of extracted preferences
        def filter_extracted_preference_info(p_match, preference, threshold, extracted):  # don't repeat code
            flag = False
            for elem in p_match:
                # If we are sure of something we add it and discard anything else
                if elem[1] <= self.levenshteinEditDistance:
                    extracted[preference].append(elem[0])
                    flag = True
                # Reject anything above our threshold
                elif flag or elem[1] > threshold:
                    break
                # Store separately possible spelling mistakes and await confirmation
                elif not flag:
                    self.g_distant[preference].append(elem[0])
            return flag, extracted

        food_found, extracted = filter_extracted_preference_info(food_match, self.FOOD, threshold, extracted)
        pricerange_found, extracted = filter_extracted_preference_info(pricerange_match, self.PRICERANGE, threshold, extracted)
        area_found, extracted = filter_extracted_preference_info(area_match, self.AREA, threshold, extracted)

        return extracted

    def next_state(self, current_state, current_act):
        """
        Decide what the next state should be based on current state and dialog act
        Input
        current_state: <str> current dialog state
        current_act: <str> dialog act extracted from the user input
        Output: <str> next dialog state
        """
        next_state = ""
        handler = self.DIALOG_ACTS.get(current_act, self.INVALIDACT_ACT)
        # Refer to "Handlers for the different dialog acts"
        next_state = handler(current_state)
        return next_state

    def generate_utterance(self, current_state, current_input):
        """
        Build the next utterance based on the current state of the dialog
        Input:
        state: <str> next dialog state
        Output: <str> next system utterance
        """
        utterance = ""
        handler = self.g_system_states.get(current_state, self.INVALIDSTATE_STATE)
        # Refer to "Handlers for the different dialog acts"
        utterance = handler(current_input)
        return utterance

    #######################################
    #### USER ACT IDENTIFICATION NEEDS ####
    #######################################
    def prepareDataSet(self, fileName):
        """
        Prepare the dataset found in fileName.
        File initially contains lines with "act utterance" distribution
        This will split the acts and utterances on two separate lists but 
        matching the indexes so labels[i] is the label for utterances[i]
        Input: 
        fileName: <str> path to file containing the dialog data
        Output: 
        labels: <[str]> list of labels
        utterances: <[str]> list of utterances
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
        """
        Load the tokenizer and train it on the fileName data
        Input: 
        fileName: <str> path to file containing dialog data
        Output: 
        tokenizer: tool that allows to vectorize a text corpus, by turning each text into a vector 
                   where the coefficient for each token is based on word count (in our case)
        encoder: tool that encodes labels with value between 0 and n_classes-1. 
        """
        labels, utterances = self.prepareDataSet(fileName)

        tokenizer = Tokenizer(num_words=self.MAX_WORDS)
        tokenizer.fit_on_texts(utterances)

        encoder = LabelEncoder()
        encoder.fit(labels)

        return tokenizer, encoder
    
    def __initModel(self):
        """
        Initialize the keyword matching baseline model
        """
        self.baseline_model = {}
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
        reqalts_keywords = ["another", "about", "else"]
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
        
        self.baseline_model[self.ACK_ACT] = ack_keywords
        self.baseline_model[self.AFFIRM_ACT] = affirm_keywords
        self.baseline_model[self.BYE_ACT] = bye_keywords
        self.baseline_model[self.CONFIRM_ACT] = confirm_keywords
        self.baseline_model[self.DENY_ACT] = deny_keywords
        self.baseline_model[self.HELLO_ACT] = hello_keywords
        self.baseline_model[self.INFORM_ACT] = inform_keywords
        self.baseline_model[self.NEGATE_ACT] = negate_keywords
        self.baseline_model[self.NULL_ACT] = null_keywords
        self.baseline_model[self.REPEAT_ACT] = repeat_keywords
        self.baseline_model[self.REQUALTS_ACT] = reqalts_keywords
        self.baseline_model[self.REQMORE_ACT] = reqmore_keywords
        self.baseline_model[self.REQUEST_ACT] = request_keywords
        self.baseline_model[self.RESTART_ACT] = restart_keywords
        self.baseline_model[self.THANKYOU_ACT] = thankyou_keywords
    
        return 

    def __keywordMatching(self, utterance, repetition = False):
        """
        Use the keyword matching baseline to find the dialog act of the input
        Input:
        model: {<str>, [<str>]} dictionary of dialog acts and keywords
        utterance: <str> user input
        repetition: <bool> should repetition of words be counted towards word count
        Output: <str> dialog act identified
        """
    
        utterance_keywords = utterance.split(" ")
        
        utterance_matches = {} #not really used but could be handy 
        utterance_matches_len = {}
        
        if repetition == False:
            for dialog_act in self.baseline_model:
                matches = set(self.baseline_model[dialog_act]).intersection(utterance_keywords)
                utterance_matches[dialog_act] = matches
                utterance_matches_len[dialog_act] = len(matches)
        else:
            for dialog_act in self.baseline_model:
                matches = 0
                for keyword in self.baseline_model[dialog_act]:
                    matches = matches + utterance_keywords.count(keyword)
                utterance_matches[dialog_act] = set(self.baseline_model[dialog_act]).intersection(utterance_keywords)
                utterance_matches_len[dialog_act] = matches
        max_matches = max(utterance_matches_len.values())
        dialog_matches = [ k for k, v in utterance_matches_len.items() if v == max_matches]
        
        if len(dialog_matches) == len(self.baseline_model):
            act = "null"
        else:
            act = dialog_matches[0][:dialog_matches[0].index('_')]
        
        return act

##############
#### MAIN ####
##############
if __name__ == "__main__":

    # Configuration bullets
    # TODO might need some local adjustments
    config = {"modelFile": './dcnn_model.h5',
              "trainFileName": './dialogs.txt',
              "ontologyFile": './ontology_dstc2.json',
              "restaurantInfoFile": './restaurantinfo.csv',
              'levenshteinEditDistance': 0,
              'lowerCase': True,
              'baseline': False,
              'outputAllCaps': True}


    dialog = Dialog(config)
    dialog.init_dialog()