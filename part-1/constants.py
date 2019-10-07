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

# Values used in common with the ontolgy.json files
REQUESTABLE = "requestable"
INFORMABLE = "informable"
FOOD = "food"
PRICERANGE = "pricerange"
AREA = "area"

# Patterns for pattern matching
PATTERNS_INFORM = [
    r"[I|i]'m looking for ([\w+\s]+)food",
    r"[I|i] want a restaurant that serves ([\w+\s]+)[food]?",
    r"[I|i] want a restaurant serving ([\w+\s]+)[food]?",
    r"[I|i]'m looking for a restaurant in the (\w+)",
    r"[I|i] would like an? ([\w+\s]+)restaurant in the (\w+) (part)? of town",
    r"[I|i]'m looking for an? (\w+) (priced)? restaurant in the (\w+) (part)? of town",
    r"[I|i]'m looking for a restaurant in (\w)+ (area|part)? that serves ([\w+\s]+)(food)?",
    r"[C|c]an [I|i] have an? ([\w+\s]+)restaurant",
    r"[I|i]'m looking for a[n]? ([\w+\s]+)restaurant and it should serve ([\w+\s]+)food",
    r"[I|i] need an? ([\w+\s]+)restaurant that is (\w+) priced",
    r"[I|i]'m looking for an? (\w+) priced restaurant with (\w+) food",
    r"[W|w]hat is an? ([\w+\s]+)restaurant in the (\w+) (part|area) of town",
    r"[W|w]hat about (\w+) food",
    r"[I|i] wanna find an? (\w+) restaurant",
    r"[I|i]'m looking for ([\w+\s]+)food please",
    r"[F|f]ind an? ([\w+\s]+)restaurant in the (\w+)"
]