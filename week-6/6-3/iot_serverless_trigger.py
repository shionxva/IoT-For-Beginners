
import logging
import os
import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

IOT_HUB_CONN_STR = os.environ.get("IOT_HUB_CONN_STR", "YOUR_SERVICE_CONNECTION_STRING")
DEVICE_ID = os.environ.get("DEVICE_ID", "YOUR_DEVICE_ID")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing LUIS request for IoT Command.')

    try:
        req_body = req.get_json()
        top_intent = req_body.get('prediction', {}).get('topIntent')

        if top_intent == 'CancelTimer':
            logging.info("Intent 'CancelTimer' detected. Sending command to IoT Device...")
            
            # Connect to IoT Hub Registry Manager
            registry_manager = IoTHubRegistryManager(IOT_HUB_CONN_STR)
            
            # Define the method name exactly as the device expects it
            device_method = CloudToDeviceMethod(method_name="cancel_timer", payload={})
            
            # Invoke the method on the device
            response = registry_manager.invoke_device_method(DEVICE_ID, device_method)
            
            logging.info(f"Device responded with status: {response.status}")
            
            return func.HttpResponse(
                f"Successfully sent cancel command to device. Device status: {response.status}",
                status_code=200
            )
            
        return func.HttpResponse("Intent processed, but no device action required.", status_code=200)

    except Exception as e:
        logging.error(f"Error invoking device method: {e}")
        return func.HttpResponse("Failed to send command to device.", status_code=500)
