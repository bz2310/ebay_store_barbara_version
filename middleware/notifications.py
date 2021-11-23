from flask import Flask, request
import requests, json

def process_message(msg, timestamp):
    js = json.loads(msg)
    ## handle message

def sns():
    try:
        js = json.loads(request.data)
    except:
        pass

    header = request.headers.get("X-Amz-Sns-Message-Type")

    if header == 'Notification':
        process_message(js['Message', js['Timestamp']])