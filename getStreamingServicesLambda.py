import math
import dateutil.parser
import datetime
import time
import os
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
# --------------------------------------------------------------------------------------------
# Interact with bot here 

def userSubscibedServices(intent_request):
    
    hasNetflix = get_slots(intent_request)["hasNetflix"]
    hasHulu = get_slots(intent_request)["hasHulu"]
    hasPrime = get_slots(intent_request)["hasPrime"]

    
    subscriptions = []
    
    #Makes list so bot can confirm subscriptions to User
    if hasNetflix == 'yes':
        subscriptions.append("Netlfix")
        
    if hasHulu == 'yes':
        subscriptions.append("Hulu")
        
    if hasPrime == 'yes':
        subscriptions.append("Amazon Prime")
        
    #Converts list of subscriptions to a string    
    subscriptionsSting = ''.join(subscriptions)
    
    
        
      # Currently returns subscriptions to User, this is where we would do backend service when we are ready
    return close(intent_request['sessionAttributes'],
                     'Fulfilled',
                     {'contentType': 'PlainText',
                      'content': 'Ok, thank you. I know now you are subscribed to {}, '.format(subscriptionsSting)})

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    #logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'getPreferences':
        return userSubscibedServices(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
        # By default, treat the user request as coming from the America/New_York time zone.
    #os.environ['TZ'] = 'America/New_York'
    #time.tzset()
    #logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)