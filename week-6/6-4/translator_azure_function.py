
import logging
import os
import json
import requests
import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Message

# Environment variables
TRANSLATOR_ENDPOINT = os.environ["TRANSLATOR_ENDPOINT"]
TRANSLATOR_KEY = os.environ["TRANSLATOR_KEY"]
TRANSLATOR_REGION = os.environ["TRANSLATOR_REGION"]
IOT_HUB_CONN_STR = os.environ["IOT_HUB_CONN_STR"]

def translate_text(text, source_lang, target_lang):
    path = '/translate'
    constructed_url = TRANSLATOR_ENDPOINT + path
    params = {
        'api-version': '3.0',
        'from': source_lang,
        'to': [target_lang]
    }
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_REGION,
        'Content-type': 'application/json'
    }
    body = [{'text': text}]
    
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']

def main(event: func.EventHubEvent):
    # This function triggers when a device sends telemetry to the IoT Hub
    try:
        message_body = event.get_body().decode('utf-8')
        data = json.loads(message_body)
        
        original_text = data.get('text')
        source_lang = data.get('source_lang') # e.g., 'vi' or 'de'
        target_lang = data.get('target_lang') # e.g., 'de' or 'vi'
        target_device = data.get('target_device') # ID of the other device
        
        logging.info(f"Received speech from {source_lang}. Translating to {target_lang}...")
        
        # 1. Translate the text
        translated_text = translate_text(original_text, source_lang, target_lang)
        logging.info(f"Translated text: {translated_text}")
        
        # 2. Send the translated text to the target IoT device via C2D message
        registry_manager = IoTHubRegistryManager(IOT_HUB_CONN_STR)
        msg = Message(translated_text)
        msg.custom_properties["language"] = target_lang
        
        registry_manager.send_c2d_message(target_device, msg)
        logging.info(f"Successfully routed translated message to {target_device}")

    except Exception as e:
        logging.error(f"Error processing translation routing: {e}")
