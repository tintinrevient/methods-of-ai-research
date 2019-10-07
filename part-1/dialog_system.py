import Levenshtein
import json, csv, yaml, random, operator, re
import numpy as np
from keras.models import load_model
from classifier import load_tokenizer_and_encoder
import constants, keywords

class Dialog:

    def __init__(self, config):

        with open("config.yml", 'r') as file:
            yaml_config = yaml.load(file, Loader=yaml.BaseLoader)

        self.model = load_model(yaml_config["path"]["model"])
        self.tokenizer, self.encoder = load_tokenizer_and_encoder(yaml_config["path"]["label_dialogs"]["train"])
        self.ontology = json.loads(open(yaml_config["path"]["ontology"]).read())
        self.restaurant_list = self._load_restaurant_info(yaml_config["path"]["restaurant_info_file"])

        self.levenshtein_edit_distance = config["levenshtein_edit_distance"]
        self.lowercase = config["lowercase"]
        self.baseline = config["baseline"]
        self.output_all_caps = config["output_all_caps"]
        self.all_preferences_recognized = config["all_preferences_recognized"]

        self.preferences = {
            constants.FOOD: [],
            constants.AREA: [],
            constants.PRICERANGE: []
        }

        self.available_restaurants = []

        # Possible spelling mistake being questioned
        self.mistake = []

        # Preference being questioned for mistakes atm
        self.preference_at_stake = ""

        # Currently selected restaurant for suggestion and/or description
        self.selected_restaurant = ""

        # Flag that checks updates on preferences
        self.updates = False

        # User possible spelling mistakes
        self.distance = {
            constants.FOOD: [],
            constants.AREA: [],
            constants.PRICERANGE: []
        }

        self.baseline_model = ""

        # {<User dialog act, next_state determining function>} dictionary
        self.DIALOG_ACTS = {
            constants.ACK_ACT: self._ack,
            constants.AFFIRM_ACT: self._affirm,
            constants.BYE_ACT: self._bye,
            constants.CONFIRM_ACT: self._confirm,
            constants.DENY_ACT: self._deny,
            constants.HELLO_ACT: self._hello,
            constants.INFORM_ACT: self._inform,
            constants.NEGATE_ACT: self._negate,
            constants.NULL_ACT: self._null,
            constants.REPEAT_ACT: self._repeat,
            constants.REQALTS_ACT: self._reqalts,
            constants.REQUEST_ACT: self._request,
            constants.RESTART_ACT: self._restart,
            constants.THANKYOU_ACT: self._thankyou
        }

        # {<Dialog state, utterance generation function>} dictionary
        self.system_states = {
            constants.WELCOME_STATE: self._welcome,
            constants.INFORM_NO_MATCHES_STATE: self._inform_no_matches,
            constants.REQUEST_MISSING_PREFERENCES_STATE: self._request_missing_preferences,
            constants.SUGGEST_RESTAURANT_STATE: self._suggest_restaurant,
            constants.PROVIDE_DESCRIPTION_STATE: self._provide_description,
            constants.CLOSURE_STATE: self._closure
        }

        # Compilations of the patterns above
        self.PATTERNS_INFORM_COMPILED = []
        for i in range(len(constants.PATTERNS_INFORM)):
            self.PATTERNS_INFORM_COMPILED.append(re.compile(constants.PATTERNS_INFORM[i]))


    #############################################################
    #### NEXT STATE DETERMINING FUNCTIONS (FROM DIALOG ACTS) ####
    #############################################################
    # Handlers for the different dialog acts
    # Input:
    # current_state: <str> current dialog state
    # Output: <str> next dialog state

    def _ack(self, current_state):
        if current_state == constants.WELCOME_STATE:
            next_state = constants.WELCOME_STATE
        elif current_state == constants.INFORM_NO_MATCHES_STATE:
            next_state = constants.INFORM_NO_MATCHES_STATE
        elif current_state == constants.REQUEST_MISSING_PREFERENCES_STATE:
            next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
        elif current_state == constants.SUGGEST_RESTAURANT_STATE:
            next_state = constants.SUGGEST_RESTAURANT_STATE
        elif current_state == constants.PROVIDE_DESCRIPTION_STATE:
            next_state = constants.PROVIDE_DESCRIPTION_STATE
        elif current_state == constants.CLOSURE_STATE:
            next_state = constants.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self._system_print(sentence)

            next_state = constants.CLOSURE_STATE

        return next_state


    def _affirm(self, current_state):
        if current_state == constants.WELCOME_STATE:
            next_state = constants.WELCOME_STATE
        elif current_state == constants.INFORM_NO_MATCHES_STATE:
            next_state = constants.INFORM_NO_MATCHES_STATE
        elif current_state == constants.REQUEST_MISSING_PREFERENCES_STATE:
            # User is answering a question on possible mistakes
            self._set_preference(self.preference_at_stake, self.mistake)
            self.preference_at_stake = ""
            self.mistake = []

            if len([i for i in list(self.preferences.values()) if len(i) > 0]) < 1:
                next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
            elif self.all_preferences_recognized and len([i for i in list(self.preferences.values()) if len(i) > 0]) < 3:
                next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
            else:
                # Perform the lookup of restaurants in the DB
                self.available_restaurants = self._find_possible_restaurants()
                # Check for availability
                if len(self.available_restaurants) == 0:
                    next_state = constants.INFORM_NO_MATCHES_STATE
                else:
                    next_state = constants.SUGGEST_RESTAURANT_STATE

        elif current_state == constants.SUGGEST_RESTAURANT_STATE:
            next_state = constants.SUGGEST_RESTAURANT_STATE
        elif current_state == constants.PROVIDE_DESCRIPTION_STATE:
            next_state = constants.PROVIDE_DESCRIPTION_STATE
        elif current_state == constants.CLOSURE_STATE:
            next_state = constants.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self._system_print(sentence)

            next_state = constants.CLOSURE_STATE

        return next_state


    def _bye(self, current_state):
        next_state = constants.CLOSURE_STATE
        return next_state


    def _confirm(self, current_state):
        if current_state == constants.WELCOME_STATE:
            next_state = constants.WELCOME_STATE
        elif current_state == constants.INFORM_NO_MATCHES_STATE:
            next_state = constants.INFORM_NO_MATCHES_STATE
        elif current_state == constants.REQUEST_MISSING_PREFERENCES_STATE:
            next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
        elif current_state == constants.SUGGEST_RESTAURANT_STATE:
            next_state = constants.PROVIDE_DESCRIPTION_STATE
        elif current_state == constants.PROVIDE_DESCRIPTION_STATE:
            next_state = constants.PROVIDE_DESCRIPTION_STATE
        elif current_state == constants.CLOSURE_STATE:
            next_state = constants.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self._system_print(sentence)

            next_state = constants.CLOSURE_STATE

        return next_state


    def _deny(self, current_state):
        if current_state == constants.WELCOME_STATE:
            # The program was opened by mistake, we take
            next_state = constants.CLOSURE_STATE
        elif current_state == constants.INFORM_NO_MATCHES_STATE:
            next_state = constants.INFORM_NO_MATCHES_STATE
        elif current_state == constants.REQUEST_MISSING_PREFERENCES_STATE:
            next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
        elif current_state == constants.SUGGEST_RESTAURANT_STATE:
            # TODO
            # TODO Extract relevant information
            # TODO update preferences if no updates this is actually reqalts
            # Check preferences again and act accordingly
            if len([i for i in list(self.preferences.values()) if len(i) < 1]) > 0:  # We could land here, not redundant
                next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
            else:
                # Perform the lookup of restaurants in the db
                self.available_restaurants = self._find_possible_restaurants()
                # Check for availability
                if len(self.available_restaurants) == 0:
                    next_state = constants.INFORM_NO_MATCHES_STATE
                else:
                    next_state = constants.SUGGEST_RESTAURANT_STATE

            next_state = constants.SUGGEST_RESTAURANT_STATE

        elif current_state == constants.PROVIDE_DESCRIPTION_STATE:
            # TODO like SUGGEST_RESTAURANT_STATE?
            next_state = constants.PROVIDE_DESCRIPTION_STATE
        elif current_state == constants.CLOSURE_STATE:
            next_state = constants.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self._system_print(sentence)

            next_state = constants.CLOSURE_STATE

        return next_state


    def _hello(self, current_state):
        return current_state

    # After an inform act only no matches or suggest are possible states
    # Moreover, inform act can be input from any other state
    def _inform(self, current_state):
        if current_state == constants.CLOSURE_STATE:
            next_state = constants.CLOSURE_STATE
        else:
            # Check constraints
            # CONFIGURATION POINT
            if len([i for i in list(self.preferences.values()) if len(i) < 1]) > 0:
                next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
            else:
                # Perform the lookup of restaurants in the db
                self.available_restaurants = self._find_possible_restaurants()
                # Check for availability
                if len(self.available_restaurants) == 0:
                    next_state = constants.INFORM_NO_MATCHES_STATE
                else:
                    next_state = constants.SUGGEST_RESTAURANT_STATE
        return next_state


    # TODO
    def _negate(self, current_state):
        if current_state == constants.WELCOME_STATE:
            next_state = constants.WELCOME_STATE
        elif current_state == constants.INFORM_NO_MATCHES_STATE:
            next_state = constants.INFORM_NO_MATCHES_STATE
        elif current_state == constants.REQUEST_MISSING_PREFERENCES_STATE:
            # User is answering a question on possible mistakes
            self.mistake = []
            self.preference_at_stake = ""
            next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
        elif current_state == constants.SUGGEST_RESTAURANT_STATE:
            # This is actually reqalts
            next_state = constants.SUGGEST_RESTAURANT_STATE
        elif current_state == constants.PROVIDE_DESCRIPTION_STATE:
            # This is actually inform
            next_state = constants.PROVIDE_DESCRIPTION_STATE
        elif current_state == constants.CLOSURE_STATE:
            next_state = constants.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self._system_print(sentence)

            next_state = constants.CLOSURE_STATE

        return next_state


    def _null(self, current_state):
        return current_state


    def _repeat(self, current_state):
        return current_state


    # TODO
    def _reqalts(self, current_state):
        if current_state == constants.CLOSURE_STATE:
            next_state = constants.CLOSURE_STATE
        else:
            # Check constraints
            # CONFIGURATION POINT
            if len([i for i in list(self.preferences.values()) if len(i) > 0]) < 1:
                next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
            elif self.all_preferences_recognized and len([i for i in list(self.preferences.values()) if len(i) > 0]) < 3:
                next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
            else:
                # Check for availability
                if len(self.available_restaurants) == 0:
                    next_state = constants.INFORM_NO_MATCHES_STATE
                else:
                    next_state = constants.SUGGEST_RESTAURANT_STATE

        return next_state

    def _reqmore(self, current_state):
        if current_state == constants.WELCOME_STATE:
            next_state = constants.WELCOME_STATE
        elif current_state == constants.INFORM_NO_MATCHES_STATE:
            next_state = constants.INFORM_NO_MATCHES_STATE
        elif current_state == constants.REQUEST_MISSING_PREFERENCES_STATE:
            next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
        elif current_state == constants.SUGGEST_RESTAURANT_STATE:
            next_state = constants.SUGGEST_RESTAURANT_STATE
        elif current_state == constants.PROVIDE_DESCRIPTION_STATE:
            next_state = constants.PROVIDE_DESCRIPTION_STATE
        elif current_state == constants.CLOSURE_STATE:
            next_state = constants.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self._system_print(sentence)

            next_state = constants.CLOSURE_STATE

        return next_state

    def _request(self, current_state):
        if current_state == constants.WELCOME_STATE:
            next_state = constants.WELCOME_STATE
        elif current_state == constants.INFORM_NO_MATCHES_STATE:
            next_state = constants.INFORM_NO_MATCHES_STATE
        elif current_state == constants.REQUEST_MISSING_PREFERENCES_STATE:
            next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
        elif current_state == constants.SUGGEST_RESTAURANT_STATE:
            next_state = constants.PROVIDE_DESCRIPTION_STATE
        elif current_state == constants.PROVIDE_DESCRIPTION_STATE:
            next_state = constants.PROVIDE_DESCRIPTION_STATE
        elif current_state == constants.CLOSURE_STATE:
            next_state = constants.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self._system_print(sentence)

            next_state = constants.CLOSURE_STATE

        return next_state

    def _restart(self, current_state):
        self._reset_preferences()
        self._dump_restaurants_list()
        next_state = constants.WELCOME_STATE

        return next_state


    def _thankyou(self, current_state):
        if (current_state == constants.WELCOME_STATE):
            next_state = constants.WELCOME_STATE
        elif (current_state == constants.INFORM_NO_MATCHES_STATE):
            next_state = constants.INFORM_NO_MATCHES_STATE
        elif (current_state == constants.REQUEST_MISSING_PREFERENCES_STATE):
            next_state = constants.REQUEST_MISSING_PREFERENCES_STATE
        elif (current_state == constants.SUGGEST_RESTAURANT_STATE):
            next_state = constants.CLOSURE_STATE
        elif (current_state == constants.PROVIDE_DESCRIPTION_STATE):
            next_state = constants.CLOSURE_STATE
        elif (current_state == constants.CLOSURE_STATE):
            next_state = constants.CLOSURE_STATE
        else:
            sentence = "Generic error message generated when transitioning states"
            self._system_print(sentence)

            next_state = constants.CLOSURE_STATE

        return next_state


    # Fallback for the handler when act is not correctly classified as a valid act
    # Which in theory should never happen
    def _invalidact(self, current_state):
        sentence = "Something went terribly wrong. We shouldn't have found this unreachable act!"
        self._system_print(sentence)

        next_state = constants.CLOSURE_STATE
        return next_state

    ################################################
    #### SYSTEM UTTERANCES GENERATION FUNCTIONS ####
    ################################################
    # Dialog state nodes utterances generation handlers
    # Input:
    # utterance: <str> current user input
    # Output: <str> next system utterance

    def _welcome(self, utterance):
        return "Welcome to the restaurant selection assistant. Please enter your preferences."


    def _inform_no_matches(self, utterance):
        if len(self.available_restaurants) == 0:
            no_matches = "There are no %s restaurants in the %s price range located in the %s." % (
                self.preferences[constants.FOOD], self.preferences[constants.PRICERANGE], self.preferences[constants.AREA])
        return no_matches


    def _request_missing_preferences(self, utterance):
        missing = []
        # See what preferences are missing
        if not self.preferences[constants.FOOD]:
            missing.append(constants.FOOD)
        if not self.preferences[constants.AREA]:
            missing.append(constants.AREA)
        if not self.preferences[constants.PRICERANGE]:
            missing.append(constants.PRICERANGE)
        # Check if we have possible spelling mistakes

        if self._possible_mistakes():
            request_preferences = self._question_spelling_mistakes()
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
    def _possible_mistakes(self):
        return len(self.distance[constants.FOOD]) + len(self.distance[constants.PRICERANGE]) + len(self.distance[constants.AREA])


    def _question_spelling_mistakes(self):
        """
        Create a question based on stored spelling mistakes, if there are any.
        Output: <str> question if there are possible mistakes in distance, 0 otherwise
        """
        # Check if we have possible misspellings
        question = self._spelling_mistakes(constants.FOOD)
        if not question:  # Keep in mind that 0 evaluates to False
            question = self._spelling_mistakes(constants.PRICERANGE)
            if not question:
                question = self._spelling_mistakes(constants.AREA)
        return question


    def _spelling_mistakes(self, preference):
        """
        Spelling mistakes per preference
        Input:
        preference: <str> preference to check in distance
        Output: <str> question if there are possible mistakes in distance[preference], 0 otherwise
        """
        # Make extra sure we are not recycling by any chance
        self.g_mistake = []
        self.g_preference_at_stake = ""

        question = 0
        if len(self.distance[preference]) > 0:
            mistakes = self.distance[preference][0]
            for value in self.distance[preference]:
                self.g_mistake.append(value)
                if mistakes == value:
                    continue  # This is only done for the pretty printing
                mistakes = mistakes + ', ' + value  # this pretty printing

            question = "I did not understand some of what you said. Did you mean %s %s?" % (mistakes, preference)

            self.preference_at_stake = preference
            self.distance[preference] = []
        return question


    def _suggest_restaurant(self, utterance):
        if len(self.available_restaurants) == 0:
            suggest = "There are no restaurants left with those preferences"
        else:
            ran_restaurant = random.randint(1, len(self.available_restaurants)) - 1
            self.selected_restaurant = self.available_restaurants[ran_restaurant]
            self.available_restaurants.remove(self.selected_restaurant)
            suggest = "%s is a %s restaurant in the %s of the city and the prices are in the %s range" % (
                self.selected_restaurant[0], self.selected_restaurant[3], self.selected_restaurant[2],
                self.selected_restaurant[1])
        return suggest


    def _provide_description(self, utterance):
        description = []
        descriptionname = []
        request_description = utterance.split(" ")
        # Check for description requests in current input
        for d in request_description:
            if self._check_description_elements(d, constants.PRICERANGE):
                description.append(self.selected_restaurant[1])
                descriptionname.append(constants.PRICERANGE)
            if self._check_description_elements(d, constants.AREA):
                description.append(self.selected_restaurant[2])
                descriptionname.append(constants.AREA)
            if self._check_description_elements(d, constants.FOOD):
                description.append(self.selected_restaurant[3])
                descriptionname.append(constants.FOOD)
            if self._check_description_elements(d, constants.PHONENUMBER):
                description.append(self.selected_restaurant[4])
                descriptionname.append(constants.PHONENUMBER)
            if self._check_description_elements(d, constants.ADDRESS):
                description.append(self.selected_restaurant[5])
                descriptionname.append(constants.ADDRESS)
            if self._check_description_elements(d, constants.POSTCODE):
                description.append(self.selected_restaurant[6])
                descriptionname.append(constants.POSTCODE)
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


    def _check_description_elements(self, word, ontology_subset):
        """
        Check if a word matches a certain ontology subset
        Input:
        word: <str> word to check
        ontology_subset: <str> [AREA | PRICERANGE | FOOD]
        Output: <bool> True if it matches, False otherwise
        """
        checks_out = word == ontology_subset or word in self.ontology[constants.INFORMABLE][ontology_subset]
        return checks_out


    def _check_details_elements(self, word, details_subset):
        """
        Check if a word matches a certain details expressions subset
        Input:
        word: <str> word to check
        ontology_subset: <str> [PHONENUMBER | POSTCODE | ADDRESS]
        Output: <bool> True if it matches, False otherwise
        """
        checks_out = word == details_subset or word in constants.DETAILS_EXPRESSIONS[details_subset]
        return checks_out


    def _closure(self, utterance):
        sentence = "Good bye"
        return sentence


    # Fallback for the handler when next_state is not correctly determined as a valid state
    # Which in theory should never happen
    def _invalidstate(self, utterance):
        sentence = "An error occurred, please report log"
        result = "Something went terribly wrong. This is an unreachable dialog state!"
        self._system_print(sentence.upper())
        return result


    def _load_restaurant_info(self, csvfile):

        with open(csvfile, 'r') as file:
            restaurant_list = list(csv.reader(file))

        return restaurant_list[1:]


    def _system_print(self, utterance):

        if self.output_all_caps:
            print(utterance.upper())
        else:
            print(utterance)


    def _find_possible_restaurants(self):
        """
        Lookup possible restaurants with the given contraints in the preferences
        Output: <[str]> list of restaurants that match the preferences
        """
        restaurants = []
        preference_keys = [k for (k, v) in list(self.preferences.items()) if len(v) > 0]

        goal = len(preference_keys)

        for row in self.restaurant_list:

            counter = 0
            for preference_key in preference_keys:
                if self.preferences[preference_key] in row:
                    counter += 1

            if counter == goal:
                restaurants.append(row)

        return restaurants


    def _set_preference(self, preference, value):
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

        if preference in self.preferences and self.preferences[preference] != value:
            self.preferences[preference] = value
            setting = True
            self._dump_restaurants_list()
        else:
            setting = False

        return setting


    def _reset_preferences(self):
        """
        Restart preferences
        Output: <bool> success resetting
        """
        success = False
        self._dump_restaurants_list()

        self.preferences = {
            constants.FOOD: [],
            constants.AREA: [],
            constants.PRICERANGE: []
        }

        self.updates = False
        success = True
        return success


    def _dump_restaurants_list(self):
        """
        Reset the available restaurants array
        Output: <bool> success resetting
        """
        success = False
        self.available_restaurants = []
        self.selected_restaurant = ""
        success = True
        return success


    ##########################################
    #### DIALOG TRANSITION CORE FUNCTIONS ####
    ##########################################
    def init_dialog(self):
        """
        Start a dialog
        """
        # Preprare dialog assistant
        # 1. Make sure we don't recicle
        self._reset_preferences()
        next_state = ""
        next_system_utterance = ""
        if self.baseline:
            self.baseline_model = keywords.init_model()

        # 2. Initialize dialog
        current_state = constants.WELCOME_STATE  # Initial dialog state
        next_system_utterance = self._welcome("")  # Initial system utterance
        self._system_print(next_system_utterance)
        try:
            while current_state != constants.CLOSURE_STATE:
                current_input = input()
                if self.lowercase == True:
                    current_input = current_input.lower()

                next_state, next_system_utterance = self._dialog_transition(current_state, current_input)
                current_state = next_state
                self._system_print(next_system_utterance)

        except KeyboardInterrupt:
            pass


    def _dialog_transition(self, current_state, current_input):
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
        self.updates = True
        next_dialog_state = ""
        next_system_utterance = ""

        current_act = self._get_act(current_input)
        if current_act in constants.INFORMING_ACTS:
            self.updates = self._manage_info(current_input)
        next_dialog_state = self._next_state(current_state, current_act)
        next_system_utterance = self._generate_utterance(next_dialog_state, current_input)

        # Next is a special case
        if current_act == constants.REQALTS_ACT and next_dialog_state == constants.INFORM_NO_MATCHES_STATE and not self.updates:
            next_system_utterance = "There are no more %s restaurants in the %s price range in the %s of the city. Please change your preferences." % (
                self.preferences[constants.FOOD], self.preferences[constants.PRICERANGE], self.preferences[constants.AREA])

        return next_dialog_state, next_system_utterance


    def _get_act(self, utterance):
        """
        Extract the dialog act from the user utterance
        Input:
        utterance: <str> current user utterance
        Output: <str> dialog act identified
        """
        if (self.baseline):
            act = keywords.keyword_matching(self.baseline_model, utterance)
            return act
        else:
            act = self.model.predict(np.array(self.tokenizer.texts_to_matrix([utterance], mode='count')))
            return self.encoder.classes_[np.argmax(act[0])]


    def _manage_info(self, current_input):
        """
        Extract possible information contained in the utterance and attempt to
        update preferences
        Input:
        current_input: <str> current user utterance
        Output: <bool> True if a preference was updated, False otherwise
        """
        extracted_info = self._extract_information(current_input)
        l_updates = False
        for preference in extracted_info:
            l_updates = self._set_preference(preference, extracted_info[preference]) or l_updates

        return l_updates


    # AUX: Extract the relevant information from the current input, focusing on a single preference
    # Input:
    # word: <str> word to evaluate
    # p_list: <[str]> list of keywords for a preference
    # threshold: <int> maximum value a word can score to enter the preferences dictionaries
    # p_match: <word, score> preferences dictionary
    # Output: p_match updated with valid word entries
    def _extract_preference_info(self, word, p_list, threshold, p_match):
        for elem in p_list:
            tmp_score = Levenshtein.distance(word, elem)
            if tmp_score < threshold:
                p_match[elem] = tmp_score
        return p_match


    # AUX: Select extracted preferences according to their edit distances
    # Input:
    # p_match: <word, score> dictionary for a preference
    # preference: <str> preference
    # threshold: <int> maxiumum score to consider
    # extraced: <preference, [str]> dictionary of extracted preferences
    # Output:
    # flag: <bool> True if any preferences found for this preference, False otherwise
    # extracted: <preference, [str]> dictionary of extracted preferences
    def _filter_extracted_preference_info(self, p_match, preference, threshold, extracted):  # don't repeat code
        flag = False
        for elem in p_match:
            # If we are sure of something we add it and discard anything else
            if elem[1] <= self.levenshtein_edit_distance:
                extracted[preference].append(elem[0])
                flag = True
            # Reject anything above our threshold
            elif flag or elem[1] > threshold:
                break
            # Store separately possible spelling mistakes and await confirmation
            elif not flag:
                self.distance[preference].append(elem[0])
        return flag, extracted


    def _extract_information(self, utterance):
        """
        Extract the relevant information from the current input
        Input:
        utterance: <str> current user utterance classified as inform
        Output: dictionary with <preference,value> pairs for g_preferences
        """
        food_list = self.ontology[constants.INFORMABLE][constants.FOOD]
        pricerange_list = self.ontology[constants.INFORMABLE][constants.PRICERANGE]
        area_list = self.ontology[constants.INFORMABLE][constants.AREA]

        words = utterance.split(" ")  # TODO pattern-matching

        # <word, score> dictionaries
        food_match = {}
        pricerange_match = {}
        area_match = {}
        # Maximum value a word can score to enter the dictionaries above
        threshold = 3  # TODO

        for pattern in self.PATTERNS_INFORM_COMPILED:
            search = pattern.search(utterance)
            if search == None:
                continue
            for group in search.groups():
                words = group.split(" ")
                for word in words:
                    word = word.strip()
                    food_match = self._extract_preference_info(word, food_list, threshold, food_match)
                    pricerange_match = self._extract_preference_info(word, pricerange_list, threshold, pricerange_match)
                    area_match = self._extract_preference_info(word, area_list, threshold, area_match)

        # If no pattern matched, we try looking for every word
        if not (len(food_match) + len(pricerange_match) + len(area_match)):
            for word in words:
                food_match = self._extract_preference_info(word, food_list, threshold, food_match)
                pricerange_match = self._extract_preference_info(word, pricerange_list, threshold, pricerange_match)
                area_match = self._extract_preference_info(word, area_list, threshold, area_match)

        food_match = sorted(food_match.items(), key=operator.itemgetter(1))
        pricerange_match = sorted(pricerange_match.items(), key=operator.itemgetter(1))
        area_match = sorted(area_match.items(), key=operator.itemgetter(1))

        # Same structure as our g_preferences and g_distant
        extracted = {
            constants.FOOD: [],
            constants.PRICERANGE: [],
            constants.AREA: []
        }

        food_found, extracted = self._filter_extracted_preference_info(food_match, constants.FOOD, threshold, extracted)
        pricerange_found, extracted = self._filter_extracted_preference_info(pricerange_match, constants.PRICERANGE, threshold,
                                                                       extracted)
        area_found, extracted = self._filter_extracted_preference_info(area_match, constants.AREA, threshold, extracted)

        return extracted


    def _next_state(self, current_state, current_act):
        """
        Decide what the next state should be based on current state and dialog act
        Input
        current_state: <str> current dialog state
        current_act: <str> dialog act extracted from the user input
        Output: <str> next dialog state
        """
        next_state = ""
        handler = self.DIALOG_ACTS.get(current_act, constants.INVALIDACT_ACT)
        # Refer to "Handlers for the different dialog acts"
        next_state = handler(current_state)
        return next_state


    def _generate_utterance(self, current_state, current_input):
        """
        Build the next utterance based on the current state of the dialog
        Input:
        state: <str> next dialog state
        Output: <str> next system utterance
        """
        utterance = ""
        handler = self.system_states.get(current_state, constants.INVALIDSTATE_STATE)
        # Refer to "Handlers for the different dialog acts"
        utterance = handler(current_input)
        return utterance


if __name__ == "__main__":

    config = {'levenshtein_edit_distance': 0,
              'lowercase': True,
              'baseline': True,
              'output_all_caps': False,
              'all_preferences_recognized': False}

    dialogs = Dialog(config)
    dialogs.init_dialog()
