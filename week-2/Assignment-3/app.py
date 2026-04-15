import json
import time
import paho.mqtt.client as mqtt
import threading
import os

id = '<ID>'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'soilmoistureserver'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

# ===== CALIBRATION CONSTANTS =====
# Update these based on your calibration results!
AVG_DECREASE_PER_SEC = 20.33  # ← REPLACE with your calculated average
TARGET_MOISTURE = 450         # Target soil moisture level
SAFETY_FACTOR = 0.9          # Run 90% of calculated time to avoid overshoot
MIN_WATER_TIME = 0.5         # Minimum pump time in seconds
MAX_WATER_TIME = 10.0        # Maximum pump time in seconds

wait_time = 20  # Time to wait for moisture to stabilize after watering
is_watering = False  # Flag to prevent multiple simultaneous waterings

def send_relay_command(client, state):
    """Send relay command to turn pump on/off"""
    command = {'relay_on': state}
    print(f"Sending: {command}")
    client.publish(server_command_topic, json.dumps(command))

def calculate_water_time(current_moisture, target_moisture):
    """
    Calculate how long to run pump based on calibration data
    """
    if current_moisture <= target_moisture:
        return 0  # Already moist enough
    
    moisture_decrease_needed = current_moisture - target_moisture
    water_time = moisture_decrease_needed / AVG_DECREASE_PER_SEC
    
    # Apply safety factor to avoid overshoot
    water_time = water_time * SAFETY_FACTOR
    
    # Clamp to min/max values
    water_time = max(MIN_WATER_TIME, min(water_time, MAX_WATER_TIME))
    
    return water_time

def control_relay(client, current_moisture):
    """Control the pump based on calculated water time"""
    global is_watering
    
    is_watering = True
    
    # Calculate required water time
    water_time_needed = calculate_water_time(current_moisture, TARGET_MOISTURE)
    
    if water_time_needed <= 0:
        print(f"soil moisture {current_moisture} is already below target {TARGET_MOISTURE}")
        is_watering = False
        return
    
    print(f"\ncurrent moisture: {current_moisture}")
    print(f"target moisture: {TARGET_MOISTURE}")
    print(f"calculated pump time: {water_time_needed:.2f} seconds")
    
    # Unsubscribe from telemetry to ignore readings during watering
    print("Unsubscribing from telemetry...")
    mqtt_client.unsubscribe(client_telemetry_topic)
    
    # Run pump
    send_relay_command(client, True)
    time.sleep(water_time_needed)
    send_relay_command(client, False)
    
    # Wait for moisture to stabilize
    print(f"Waiting {wait_time}s for moisture to stabilize...")
    time.sleep(wait_time)
    
    # Re-subscribe to telemetry
    print("Resubscribing to telemetry...")
    mqtt_client.subscribe(client_telemetry_topic)
    
    is_watering = False
    print("watering cycle complete\n")

def handle_telemetry(client, userdata, message):
    """Handle incoming telemetry messages"""
    global is_watering
    
    if is_watering:
        # Skip processing if already watering
        return
    
    try:
        payload = json.loads(message.payload.decode())
        print(f"message received: {payload}")
        
        soil_moisture = payload.get('soil_moisture')
        
        if soil_moisture and soil_moisture > TARGET_MOISTURE:
            print(f"soil moisture ({soil_moisture}) exceeds target ({TARGET_MOISTURE})")
            # Start watering in a separate thread
            threading.Thread(target=control_relay, args=(client, soil_moisture)).start()
        elif soil_moisture:
            print(f"soil moisture ({soil_moisture}) is acceptable (target: {TARGET_MOISTURE})")
            
    except Exception as e:
        print(f"Error handling telemetry: {e}")

# Load calibration data if available
def load_calibration():
    global AVG_DECREASE_PER_SEC
    try:
        with open('calibration_data.json', 'r') as f:
            data = json.load(f)
            AVG_DECREASE_PER_SEC = data['avg_decrease_per_sec']
            print(f"loaded calibration: {AVG_DECREASE_PER_SEC:.2f} decrease per second")
    except FileNotFoundError:
        print(f"⚠️ No calibration file found. Using default: {AVG_DECREASE_PER_SEC}")

# Setup MQTT
mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

# Load calibration on startup
load_calibration()

# Print configuration
print("\n" + "="*50)
print("SOIL MOISTURE CONTROL SERVER")
print("="*50)
print(f"Calibration: {AVG_DECREASE_PER_SEC:.2f} decrease per second")
print(f"Target moisture: {TARGET_MOISTURE}")
print(f"Safety factor: {SAFETY_FACTOR}")
print(f"Min/Max water time: {MIN_WATER_TIME}s / {MAX_WATER_TIME}s")
print("="*50 + "\n")

# Main loop
try:
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    print("\n\nServer stopped")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
