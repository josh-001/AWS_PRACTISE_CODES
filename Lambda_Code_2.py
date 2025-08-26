import json
import boto3
from datetime import datetime
import re
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dominos_table_bhanu')
def value_inslot(slots,sname):
    value_=slots.get(sname)
    if value_ and "value" in value_ and "interpretedValue" in value_["value"]:
        return value_["value"]["interpretedValue"]
    else:
        return "" 
        
def validate_slots(sessionattr,slots):
    ## validate number ##
    # number = slots.get('Phone_number', {}).get('value', {}).get('interpretedValue', '')
    number=value_inslot(slots,'Phone_number')
    if len(number)!=10 :
        return sessionattr,0
    sessionattr['number']=number
    ### validate name
    name=value_inslot(slots,'user_name')
    if name=="" or not name.isalpha():
        return sessionattr,1
    sessionattr['user_name']=name
    ## pizzaname
    pn=value_inslot(slots,'pizzaname')
    if pn=="" or not pn.isalpha():
        return sessionattr,2
    sessionattr['pizzaname']=pn
    ## size
    s=value_inslot(slots,'size')
    if s=="":
        return sessionattr,3
    sessionattr['size']=s
    ## quatity 
    quantity = value_inslot(slots,'quantity')
    if quantity=="":
        return sessionattr,4
    if int(quantity)>10:
        return sessionattr,4
    sessionattr['quatity']=quantity
    return sessionattr,[name,pn,s,quantity]

    
def lambda_handler(event, context):
    # TODO implement
    re_slot=["Phone_number","user_name","pizzaname","size","quantity"]
    print("E",event)
    intent_name=event['sessionState']['intent']['name']
    intent = event["sessionState"]["intent"]
    # print(intent_name)
    sessionattr = event["sessionState"]["sessionAttributes"] 
    slots=event['sessionState']['intent']['slots']
    # print(slots)
    sessionid=event.get('sessionId','Unknownsession')
    invocation_source = event.get("invocationSource")
    # print(sessionid)
    if intent_name=="pizza_order":
        if invocation_source == "DialogCodeHook":
            # number = slots.get('Phone_number', {}).get('value', {}).get('interpretedValue', '')
            sessionattr,value=validate_slots(sessionattr,slots)
            # print(type(value))
            if value in [0,1,2,3,4]:
                return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": re_slot[value]
                    },
                    "sessionAttributes":sessionattr,
                    "intent": {
                        "name": intent_name,
                        "slots": slots,
                        "state": "InProgress"
                    }
                },
                }
            elif isinstance(value,list) :
                return {
                    "sessionState": {
                        "dialogAction": {
                            "type": "Delegate"
                        },
                        "intent": {
                            "name": intent_name,
                            "slots": slots,
                            "state": "InProgress"
                        }
                    }
                }
        elif invocation_source == "FulfillmentCodeHook":
            confirmation_state = intent.get("confirmationState", "None")
            if confirmation_state == "Confirmed":
                print("Confirmed")
                return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close",
                    },
                    "intent": {
                        "name": intent_name,
                        "slots": slots,
                        "state":"Fulfilled",
                    }
                },
                 "messages": [
                        {
                            "contentType": "PlainText",
                            "content": "Your pizza order has been placed! "
                        }
                    ]
                }
            elif confirmation_state == "Denied":
                print("Denied")
                return {
                "sessionState": {
                    "sessionAttributes":sessionattr,
                    "dialogAction": 
                        {"type": "ElicitSlot",
                        "slotToElicit":"freeprompt"
                        },
                        
                    "intent": {
                        "name": "Usercanceled",
                        "state":"InProgress"
                    }
                },
                "messages": [
                        {
                            "contentType": "PlainText",
                            "content": f"Okay!, I am cancelling the order.{sessionattr}"
                        }
                    ]
                }
        
    elif intent_name=='Usercanceled':
        print("usercancelled_event",event)
        
        
        
