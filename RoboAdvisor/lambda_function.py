### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        slots = get_slots(intent_request)
        
        # Use the elicitSlot dialog action to re-prompt
        
        
        
        # for the first violation detected.
        

        ### YOUR DATA VALIDATION CODE STARTS HERE ###
        if age is not None:
            age = parse_int(age)
            if age > 65:
                return build_validation_result(
                    False,
                    "age",
                    "You are over the retirement age. You should be younger than 65 years old to use this service, "
                    "please confirm your age.",
                )
            elif age < 0:
                return build_validation_result(
                    False,
                    "age",
                    "Please enter a number greater than 0.",
                )
        

        ### YOUR DATA VALIDATION CODE ENDS HERE ###
        if investment_amount is not None: 
            investment_amount = parse_int(
                investment_amount)
            if investment_amount < 5000:
                return build_validation_result(
                    False,
                    "investment_amount",
                    "The amount entered should be greater than $5000, "
                    "please confirm your amount.",
                )
                
        


        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation

    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE STARTS HERE ###
    if riskLevel is "None":
        return initial_recommendation(True, riskLevel, "100% bonds (AGG), 0% equities (SPY)")
        
    if risk_level is "Very Low":
        return initial_recommendation(True, riskLevel, "80% bonds (AGG), 20% equities (SPY)")
    if risk_level is "Low":
        return initial_recommendation(True, riskLevel, "60% bonds (AGG), 40% equities (SPY)")
        
    if risk_level is "Medium":
        return initial_recommendation(True, riskLevel, "40% bonds (AGG), 60% equities (SPY)")
        
    if risk_level is "High":
        return initial_recommendation(True, riskLevel, "20% bonds (AGG), 80% equities (SPY)")
        
    if risk_level is "Very High":
        return initial_recommendation(True, riskLevel, "0% bonds (AGG), 100% equities (SPY)")
        
        
    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE ENDS HERE ###

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{} thank you for your information;
            based on the risk level you defined, my recommendation is to choose an investment portfolio with {}
            """.format(
                first_name, initial_recommendation
            ),
        },
    )


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "RecommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
