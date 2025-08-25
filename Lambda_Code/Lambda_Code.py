import json
import boto3
from datetime import datetime
import re
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dominos_table_bhanu')

def lambda_handler(event, context):
    # TODO implement
    print(event)
    intent_name=event['sessionState']['intent']['name']
    print(intent_name)
    slots=event['sessionState']['intent']['slots']
    # print(slots)
    sessionid=event.get('sessionId','Unknownsession')
    print(sessionid)
    if intent_name=="pizza_order":
        number = slots.get('Phone_number', {}).get('value', {}).get('interpretedValue', '')
        
        if len(number)!=12:
            print("number as:",number)
            return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "Phone_number"
                },
                "intent": {
                    "name": intent_name,
                    "slots": slots,
                    "state": "InProgress"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "incorrect phone number. Enter again"
                }
            ]
        }
            
        elif not number.startswith("91"):
            return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "Phone_number"
                },
                "intent": {
                    "name": intent_name,
                    "slots": slots,
                    "state": "InProgress"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "incorrect format. should start with 91"
                }
            ]
        }
        else :
            return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "user_name"
                },
                "intent": {
                    "name": intent_name,
                    "slots": slots,
                    "state": "InProgress"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Enter your name"
                }
            ]
        }
        
        
        # customer_name = slots.get('user_name', {}).get('value', {}).get('interpretedValue', '')
        # print(customer_name)
        
        
        # pizza_type = slots.get('pizzaname', {}).get('value', {}).get('interpretedValue', '')
        # print(pizza_type)
    
        # size = slots.get('size', {}).get('value', {}).get('interpretedValue', '')
        # print(size)
        
        # quantity = slots.get('quantity', {}).get('value', {}).get('interpretedValue', '')
        # print(quantity)
        # modify_slot = slots.get('modify')
        # print(modify_slot)
        # modify_value = modify_slot.get('value', {}).get('interpretedValue', '') if modify_slot is not None else ''
        # if modify_value.lower() == 'modify':
        #     print("modify deteted:::",modify_value.lower())
        #     slots['size'] = None 
        #     slots["modify"]=None
        #     return {
        #         "sessionState": {
        #             "dialogAction": {
        #                 "type": "ElicitSlot",
        #                 "slotToElicit": "size"
        #             },
        #             "intent": {
        #                 "name": intent_name,
        #                 "slots": slots,
        #                 "state": "InProgress"
        #             }
        #         },
        #         "messages": [
        #             {"contentType": "PlainText",
        #              "content": "Sure, what size would you like instead?"}
        #         ]
        #     }
