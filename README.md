# Wi-Fi De-authentication Attack Script

## Overview

This Python script performs a Wi-Fi de-authentication attack by sending de-authentication packets to a target device through an access point (AP). The attack forces the target to disconnect from the network, simulating a denial-of-service (DoS) attack on Wi-Fi.

## Features

- Supports targeting a specific device or broadcasting to all clients.
- Allows specifying the number of packets to send (infinite by default).
- Configurable delay between packets.
- Displays vendor information for target and gateway MAC addresses via OUI lookup.

## Prerequisites

Before running the script, ensure that:

- You have **root privileges** to send de-authentication packets.
- Your network adapter supports **monitor mode**.
- You have installed the required dependencies.

## Dependencies

The script requires the following Python libraries:

- `scapy`
- `colorama`

You can install them using:

```bash
pip install scapy colorama
```

## Usage

Run the script using the following command:

```bash
sudo python3 deauth.py -g <GATEWAY_MAC> -i <INTERFACE> [-t <TARGET_MAC>] [-c <COUNT>] [-d <DELAY>]
```

### Arguments

| Argument          | Description                                                                 |
| ----------------- | --------------------------------------------------------------------------- |
| `-g, --gateway`   | **(Required)** MAC address of the access point (e.g., `AA:BB:CC:DD:EE:FF`). |
| `-i, --interface` | **(Required)** Network interface in monitor mode.                           |
| `-t, --target`    | MAC address of the target device (optional, defaults to broadcast).         |
| `-c, --count`     | Number of de-authentication packets to send (default: `0` for infinite).    |
| `-d, --delay`     | Delay between packets in seconds (default: `0.1`).                          |

### Example Commands

1. **Attack all devices on an AP (broadcast mode):**

   ```bash
   sudo python3 deauther.py -g AA:BB:CC:DD:EE:FF -i wlan0
   ```

2. **Attack a specific target device:**

   ```bash
   sudo python3 deauther.py -g AA:BB:CC:DD:EE:FF -t 11:22:33:44:55:66 -i wlan0
   ```

3. **Send only 100 de-authentication packets:**

   ```bash
   sudo python3 deauther.py -g AA:BB:CC:DD:EE:FF -t 11:22:33:44:55:66 -i wlan0 -c 100
   ```

4. **Reduce the delay between packets:**

   ```bash
   sudo python3 deauther.py -g AA:BB:CC:DD:EE:FF -i wlan0 -d 0.05
   ```

## How It Works

- The script constructs and sends **de-authentication packets** using the `scapy` library.
- If a **target MAC address** is provided, packets are directed at that device. Otherwise, the attack is **broadcasted** to all clients.
- The **packet count** determines how many packets will be sent (`0` means infinite).
- The **vendor information** for MAC addresses is retrieved from a JSON database.
- The attack continues until interrupted (Ctrl + C).

## Screenshots

![alt text](<screenshots/Annotation 2025-03-21 221145.png>)

## Disclaimer

This script is intended for **educational and security research purposes only**. Unauthorized use against networks you do not own is illegal.

