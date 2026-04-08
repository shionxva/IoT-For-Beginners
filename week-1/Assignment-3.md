# Research: IoT Sensors and Actuators

## 1. Sensor: DHT22 (Temperature and Humidity Sensor)

The DHT22 is a popular digital sensor for measuring ambient temperature and relative humidity in IoT projects like weather stations, HVAC systems, and environmental monitoring.

### What it does
The DHT22 measures two environmental parameters:
- **Temperature** of the surrounding air.
- **Relative Humidity** (the amount of water vapor in the air relative to the maximum the air can hold at that temperature).

It processes these readings internally and outputs them as a calibrated digital signal over a single wire. It is valued for its high accuracy compared to basic sensors like the DHT11.

### Electronics/Hardware Used Inside
The sensor module integrates several components onto a small PCB:
- **Capacitive Humidity Sensor**: Measures humidity by detecting changes in electrical capacitance as moisture is absorbed.
- **NTC Thermistor (Negative Temperature Coefficient)**: A resistor whose resistance decreases as temperature increases, used for temperature measurement.
- **8-bit Microcontroller**: An onboard chip that reads the analog signals from the humidity and temperature components, performs analog-to-digital conversion, applies calibration, and outputs a single digital signal.
- **Housing**: Protects the internal components while allowing air to flow through for accurate readings.

### Analog or Digital?
**Digital**. Even though the raw sensing elements are analog, the built-in microcontroller converts the signal to a digital format. The sensor communicates using a proprietary **single-bus (1-Wire)** protocol. Some breakout boards include a pull-up resistor (typically 10kΩ) required for stable communication.

### Units and Range of Measurements
The DHT22 has a wide measurement range suitable for most environmental applications.

| Measurement | Units | Range | Accuracy | Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **Temperature** | Degrees Celsius (°C) or Fahrenheit (°F) | **-40 to +80 °C**  | **±0.5 °C** (typical)  | 0.1 °C |
| **Relative Humidity** | Percentage (%) | **0 to 100% RH**  | **±2% RH** (typical)  | 0.1% RH |

**Key Specification Notes:**
- **Sampling Rate**: Can take a new reading every 2 seconds (slower than the DHT11 which is 1Hz) .
- **Supply Voltage**: Operates on 3.3V to 5.5V DC.

---

## 2. Actuator: Standard Hobby Servo Motor (e.g., SG90 or similar)

A servo motor is an actuator that allows for precise control of angular position. It is widely used in robotics, animatronics, and automation projects.

### What it does
The servo motor converts an electrical signal into precise mechanical rotation. When commanded by a controller (like an Arduino), it moves its output shaft to a specific angle (e.g., 0°, 90°, or 180°) and holds that position against external force. Unlike a standard DC motor that spins continuously, a servo is designed for precise position control.

### Electronics/Hardware Used Inside
A standard "hobby servo" is a self-contained unit with several key components inside the plastic casing:
- **DC Motor**: A small, high-speed direct current motor that provides the rotational force.
- **Gear Train**: A series of reduction gears (often made of nylon or plastic in basic models like the SG90) that reduce the motor's high speed and increase the torque output to the output shaft.
- **Potentiometer (Pot)**: A variable resistor attached to the output shaft. It acts as a position feedback sensor, telling the control circuit the current angle of the shaft.
- **Control Circuit**: A small PCB with a microcontroller that reads the incoming PWM signal from the IoT board and compares it to the potentiometer's feedback. It then drives the DC motor to minimize the difference (closed-loop control).

### Analog or Digital?
**Digital (via PWM)**. The servo is controlled by a specific type of **digital** signal called **Pulse Width Modulation (PWM)** . The position is determined by the width of a pulse sent every 20 milliseconds (50 Hz frequency).
- A 1.0 ms pulse typically commands 0 degrees.
- A 1.5 ms pulse commands 90 degrees (center).
- A 2.0 ms pulse commands 180 degrees.

### Units and Range of Inputs/Measurements
| Parameter | Units / Range | Typical Value / Notes |
| :--- | :--- | :--- |
| **Controlled Variable** | **Angular Position** | Degrees (°) |
| **Usable Range** | **0 to 180 degrees** (Standard) | Some "continuous rotation" servos have no positional limits. |
| **Input Signal** | **Pulse Width** | **1 ms to 2 ms** (for 0° to 180°) |
| **Control Frequency** | **Hertz (Hz)** | **50 Hz** (Period = 20 ms) |
| **Torque** | **kg·cm** (or oz·in) | ~1.8 kg·cm @ 4.8V (for SG90-class servo) 
| **Operating Speed** | **Seconds/60 degrees** | ~0.1 s/60° (for SG90-class servo) |

**Key Specification Notes:**
- **Supply Voltage**: Typically 4.8V to 6.0V DC. The signal pin uses 3.3V or 5V logic.
- **Current Draw**: Can spike to 250mA or more during movement; direct connection to an IoT board's 5V pin is possible for one small servo, but a separate power supply is recommended for multiple or larger servos .