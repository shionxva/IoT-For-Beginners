
import time
import threading
from azure.iot.device import IoTHubDeviceClient, MethodResponse

CONNECTION_STRING = "YOUR_DEVICE_CONNECTION_STRING"

# Global flag to control the timer
is_timer_running = False

def start_timer(duration):
    global is_timer_running
    is_timer_running = True
    print(f"\n[Timer] Started for {duration} seconds...")
    
    for i in range(duration, 0, -1):
        if not is_timer_running:
            print("[Timer] HAS BEEN CANCELLED BY CLOUD COMMAND!")
            return
        print(f"[Timer] {i} seconds remaining...")
        time.sleep(1)
        
    print("[Timer] BEEP BEEP BEEP! Time is up!")
    is_timer_running = False

def method_request_handler(method_request, device_client):
    global is_timer_running
    
    if method_request.name == "cancel_timer":
        print("\n>> CLOUD COMMAND RECEIVED: cancel_timer")
        if is_timer_running:
            is_timer_running = False # This halts the loop in start_timer
            status = 200
            payload = {"result": True, "message": "Timer halted successfully."}
        else:
            status = 200
            payload = {"result": False, "message": "No active timer to cancel."}
            
        # Send confirmation back to the Cloud (Serverless Function)
        method_response = MethodResponse.create_from_method_request(method_request, status, payload)
        device_client.send_method_response(method_response)
        print(">> Confirmed cancellation back to cloud.\n")
    else:
        print(f"Unknown method received: {method_request.name}")

def main():
    print("Initializing IoT Device Client...")
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    device_client.connect()
    
    # Register the method handler
    device_client.on_method_request_received = lambda request: method_request_handler(request, device_client)
    
    print("Device is connected and waiting for Cloud commands.")
    print("Simulating an active timer of 30 seconds for testing...")
    
    # Run a test timer in a separate thread so the main thread can listen for commands
    timer_thread = threading.Thread(target=start_timer, args=(30,))
    timer_thread.start()
    
    try:
        # Keep the main thread alive to receive messages
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down device...")
    finally:
        device_client.disconnect()

if __name__ == "__main__":
    main()
