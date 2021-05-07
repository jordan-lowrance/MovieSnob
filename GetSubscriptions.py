import math
import dateutil.parser
import datetime
import time
import os
import logging
import boto3
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key
from decimal import Decimal


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


def delegate(session_attributes, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots,
            'message': message
        }
    }
# --------------------------------------------------------------------------------------------
# Interact with bot here 

def getUserSubscriptions(intent_request):
    
    hasNetflix = get_slots(intent_request)["hasNetflix"]
    hasHulu = get_slots(intent_request)["hasHulu"]
    hasPrime = get_slots(intent_request)["hasPrime"]
    imdbRating = get_slots(intent_request)['imdbRating']
    movieYear = get_slots(intent_request)['movieYear']

    subscriptions = []
    queryResults = []
    
    #Makes list so bot can confirm subscriptions to User
    if hasNetflix == 'yes':
        subscriptions.append("Netlfix + ")
        
    if hasHulu == 'yes':
        subscriptions.append("Hulu + ")
        
    if hasPrime == 'yes':
        subscriptions.append("Amazon Prime")
        
        
    #Converts list of subscriptions to a string    
    subscriptionsSting = ''.join(subscriptions)
    
# ==============================================================================================================================================================
    client = boto3.client('dynamodb', region_name="us-west-2")
    dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
    table = dynamodb.Table('MovieSpread')
    #response = table.query(
    #    KeyConditionExpression=Key('Year').gt(movieYear) & Key("IMDb").gt(imdbRating)    
    #)
    
    response = table.scan(
        TableName = "MovieSpread",
        ProjectionExpression = "Title, #yr, IMDb",
        ExpressionAttributeNames = {'#yr': 'Year'},
        #AttributesToGet=[
            #'Title', 'IMDb', 'Year'
            #],
        #Select='SPECIFIC_ATTRIBUTES',
        FilterExpression = Attr('Year').gt(movieYear) & Attr('IMDb').gt(Decimal(str(imdbRating)))
        #KeyConditionExpression = Key('#yr').gt(movieYear) & Key('IMDb').gt(Decimal(str(imdbRating)))
        )
    
    data = response['Items']
    
    for i in data:
        queryResults.append(i['Title'])
    
    queryResultsString = ' / '.join(queryResults)
    
     
    #return delegate(session_attributes, intent_request['currentIntent']['slots'],
     #            {'contentType': 'PlainText',
      #           'content': 'Ok, thank you. I know now you are subscribed to {}. Please type -Help me pick a movie-'.format(subscriptionsSting)}
    
    
    
    #Currently returns subscriptions to User, this is where we would do backend service when we are ready
    return close(intent_request['sessionAttributes'],
                    'Fulfilled',
                    {'contentType': 'PlainText',
                     'content': queryResultsString})

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    #logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'getUserSubscriptions':
        return getUserSubscriptions(intent_request)

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
