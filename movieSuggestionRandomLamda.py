import math
import dateutil.parser
import datetime
import time
import os
import logging
import random 


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

#session_attributes,
def close(fulfillment_state, message):
    response = {
        #'sessionAttributes': session_attributes,
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

def getRandomMovie():
    
    movies = ['Get Smart', 'The Dark Knight', 'October Sky', 'Hot Fuzz', 'The Godfather', 'Castle in the Sky']
    randomMovie = movies[random.randint(0,len(movies)-1)]
    
        
    # returns the random movie to the user
    return close(
                     'Fulfilled',
                     {'contentType': 'PlainText',
                      'content': 'Hmmm. Ok, i got it! You should watch {}'.format(randomMovie)})

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    #logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'randomMovie':
        return getRandomMovie()

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