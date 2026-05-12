
import time
import json
import threading
import azure.cognitiveservices.speech as speechsdk
from azure.iot.device import IoTHubDeviceClient, Message

# --- CONFIGURATION ---
# Change these values depending on which device you are running this on
DEVICE_ID = "Device_B"
MY_LANGUAGE = "de-DE"           # e.g., 'de-DE' for German, 'vi-VN' for Vietnamese
MY_LANG_CODE = "de"             # e.g., 'de', 'vi'
TARGET_DEVICE_ID = "Device_A"   
TARGET_LANG_CODE = "vi"         # e.g., 'vi', 'de'

IOT_CONN_STR = "YOUR_DEVICE_CONNECTION_STRING"
SPEECH_KEY = "YOUR_SPEECH_SERVICES_KEY"
SPEECH_REGION = "YOUR_SPEECH_SERVICES_REGION"

# Setup IoT Client
device_client = IoTHubDeviceClient.create_from_connection_string(IOT_CONN_STR)

# Setup Speech SDK Configs
speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
speech_config.speech_recognition_language = MY_LANGUAGE
speech_config.speech_synthesis_language = MY_LANGUAGE

def message_received_handler(message):
    """Handles incoming translated text from the Cloud and plays it via TTS"""
    translated_text = message.data.decode("utf-8")
    print(f"\n[RECEIVED TRANSLATION]: {translated_text}")
    
    # Text-to-Speech output
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    print("Playing translated audio...")
    speech_synthesizer.speak_text_async(translated_text).get()
    print("Ready for next input.\n")

def capture_and_send_speech():
    """Captures mic input, converts to text, and sends to IoT Hub"""
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    print(f"\n[{DEVICE_ID}] Speak into your microphone ({MY_LANGUAGE})...")
    result = speech_recognizer.recognize_once_async().get()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: '{result.text}'")
        
        # Package data and route to IoT Hub
        payload = {
            "text": result.text,
            "source_lang": MY_LANG_CODE,
            "target_lang": TARGET_LANG_CODE,
            "target_device": TARGET_DEVICE_ID
        }
        msg = Message(json.dumps(payload))
        device_client.send_message(msg)
        print("Message sent to IoT Hub for translation.")
        
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech recognition canceled.")

def main():
    device_client.connect()
    device_client.on_message_received = message_received_handler
    
    print("Universal Translator Device Initialized.")
    print(f"Configured as: {DEVICE_ID} ({MY_LANGUAGE}) -> Sending to {TARGET_DEVICE_ID} ({TARGET_LANG_CODE})")
    
    try:
        while True:
            input("Press [ENTER] to start recording a message to send...")
            capture_and_send_speech()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        device_client.disconnect()

if __name__ == "__main__":
    main()
