# MQTT vs. AMQP vs. HTTP/HTTPS: A Comparison for IoT

## Introduction

This document compares three common communication protocols used in IoT systems: **MQTT** (Message Queuing Telemetry Transport), **AMQP** (Advanced Message Queuing Protocol), and **HTTP/HTTPS** (Hypertext Transfer Protocol). The comparison focuses on three critical aspects for IoT deployments: power usage, security, and message persistence when connections are lost.

---

## Comparison Table

| Feature | MQTT | AMQP | HTTP/HTTPS |
| :--- | :--- | :--- | :--- |
| **Communication Pattern** | Publish/Subscribe (brokered) | Publish/Subscribe with message queues | Request/Response |
| **Transport Protocol** | TCP (or WebSockets) | TCP | TCP |
| **Default Port** | 1883 (plain), 8883 (TLS) | 5672 (plain), 5671 (TLS) | 80 (HTTP), 443 (HTTPS) |
| **Header Overhead** | Very lightweight (2 bytes min) | Moderate to high | Heavy (verbose text headers) |
| **Power Usage** | **Low** – designed for constrained devices | **Moderate to High** – heavier processing | **High** – verbose, connection overhead |
| **Security** | TLS/SSL + basic username/password | TLS/SSL + SASL + advanced authentication | TLS/SSL (HTTPS) – mature, widely adopted |
| **Message Persistence (Offline)** | **Yes** – QoS 1 & 2 with persistent sessions | **Yes** – built-in message queuing | **No** – stateless, no offline storage |
| **Library Footprint** | Small (ideal for <1 MB RAM) | Large (requires more resources) | Moderate |
| **Best For** | Sensor networks, telemetry, low-power IoT | Financial systems, industrial IoT, enterprise messaging | Web APIs, browser-based applications |

---

## MQTT vs. AMQP

### Similarities
- Both are asynchronous messaging protocols that use a publish/subscribe model with a central broker.
- Both run over TCP and support TLS/SSL for encryption.
- Both are binary protocols, making them more efficient than text-based protocols like HTTP.

### Differences

| Aspect | MQTT | AMQP |
| :--- | :--- | :--- |
| **Power Usage** | Very low – minimal header overhead and lightweight implementation, ideal for battery-powered devices with limited RAM | Higher – more complex framing and error checking requires more processing power and energy |
| **Security** | Basic – supports TLS/SSL and username/password authentication, but limited built-in security features beyond that | Advanced – supports TLS/SSL plus SASL with multiple authentication mechanisms; designed for financial-grade security |
| **Message Persistence** | Yes – via QoS levels and persistent sessions; messages can be stored for offline clients until they reconnect | Yes – built on message queuing; messages persist in queues until consumed, even if the broker restarts |
| **Message Routing** | Simple – based on topic strings with wildcards | Complex – uses exchanges, bindings, and routing keys; messages go to queues before reaching consumers |
| **Complexity** | Simple – easy to implement, small code footprint | Complex – richer feature set requires more configuration and system resources |

### When to choose which?
- **Choose MQTT** for battery-powered sensors, low-bandwidth networks, and when simplicity and low power are the main priorities.
- **Choose AMQP** for industrial IoT, financial systems, or when you need advanced routing, transactions, and enterprise-grade security.

---

## MQTT vs. HTTP/HTTPS

### Similarities
- Both can run over TCP and use TLS/SSL for encrypted communication.
- Both are widely supported by cloud platforms and programming languages.

### Differences

| Aspect | MQTT | HTTP/HTTPS |
| :--- | :--- | :--- |
| **Power Usage** | Low – persistent TCP connection with minimal keep-alive; binary protocol reduces data size significantly | High – each request requires a new TCP connection (or reusing with keep-alive); verbose text headers increase data transmission; devices polling for messages waste energy on frequent checks |
| **Security** | Moderate – TLS/SSL available, but implementation quality can vary; limited built-in authentication options beyond username/password | Advanced – mature TLS support, certificate validation widely adopted, OAuth2/OpenID Connect integration possible, proven in web-scale deployments |
| **Message Persistence** | Yes – broker stores messages for offline subscribers when using persistent sessions and QoS levels above 0 | No – stateless protocol; if a device disconnects, it misses any messages sent during that time; clients must poll the server repeatedly to check for new data |
| **Communication Model** | Asynchronous push – server pushes messages to clients as soon as they become available | Synchronous pull – client requests, server responds; inefficient for real-time updates |
| **Cloud-to-Device** | Efficient – server can push commands immediately via the persistent connection | Inefficient – device must poll the server every few seconds or minutes to receive commands |
| **Header Size** | 2-4 bytes for fixed header | Often hundreds of bytes including User-Agent, Content-Type, Cookies, and other headers |

### Message Persistence Example
- **MQTT**: A temperature sensor publishes data every minute. If the cloud server goes offline for 30 minutes, the MQTT broker stores all messages. When the server reconnects, it receives the backlog of missed data.
- **HTTP**: If the server goes offline while a sensor tries to POST data, that data is lost unless the client implements its own complex retry logic and local storage.

### When to choose which?
- **Choose MQTT** for real-time sensor data, remote control commands, low-power devices, and scenarios requiring server push or offline message storage.
- **Choose HTTP/HTTPS** for web browsers, RESTful APIs, one-off data transfers, or when integrating with existing web infrastructure where MQTT is not supported.