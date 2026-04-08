# Microcontrollers vs. Single-Board Computers

## Comparison Table

| Feature | Microcontroller (MCU) | Single-Board Computer (SBC) |
| :--- | :--- | :--- |
| **Architecture** | Harvard or von Neumann; typically 8, 16, or 32-bit | Von Neumann; 64-bit (ARM, x86, RISC-V) |
| **Operating System** | Bare metal or real-time OS (RTOS) – no full OS | Runs full operating system (Linux, Android, Windows) |
| **Processing Power** | Low (MHz range, limited RAM/Flash) | High (GHz range, GB of RAM) |
| **Primary Task** | Control, sensing, real-time responses | Computation, data processing, networking, GUI |
| **Storage** | Embedded Flash (KB to MB) | SD card, eMMC, or SSD (GB to TB) |
| **I/O Capabilities** | Direct GPIO, ADC, PWM, I2C, SPI, UART; high determinism | GPIO via expansion headers, USB, HDMI, Ethernet, Wi-Fi |
| **Power Consumption** | Very low (milliwatts to a few watts) | Moderate to high (2–15+ watts) |
| **Boot Time** | Instant or < 100 ms | 10 seconds to over a minute |
| **Cost** | $0.10 – $30 | $10 – $200+ |
| **Examples** | Arduino Uno (ATmega328P), ESP32, STM32, Raspberry Pi Pico | Raspberry Pi 4/5, BeagleBone, Orange Pi, NVIDIA Jetson Nano |

---

## Why Use a Microcontroller over an SBC?

1. **Low power & battery operation**  
   MCUs consume microamps in sleep mode, making them ideal for remote sensors, wearables, or IoT devices that must run for months or years on a coin cell or small battery.

2. **Real-time deterministic control**  
   MCUs respond to events within microseconds or nanoseconds with no OS overhead. This is critical for motor control, robotics, safety systems, or any application where missing a timing deadline causes failure.

---

## Why Use an SBC over a Microcontroller?

1. **Complex software & networking**  
   SBCs run Linux, allowing you to use high-level languages (Python, Node.js, etc.), databases, web servers, and full TCP/IP stacks. This is essential for building a web-controlled camera, network gateway, or AI inference at the edge.

2. **Multitasking & rich interfaces**  
   SBCs can simultaneously run a GUI (via HDMI), handle USB peripherals (keyboard, mouse, storage), and execute multiple processes. For projects needing a screen, file system, or heavy data processing (e.g., video streaming or machine learning), an SBC is far more practical.