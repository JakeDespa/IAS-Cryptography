# Multi-Layer Encryption Transfer System

## Overview
This project implements a secure file transfer system using a **PC (Sender) $\to$ Server $\to$ PC (Receiver)** architecture. It secures data using a custom 6-layer encryption pipeline based on the project flowchart.

### Encryption Pipeline
1. **RSA** (Asymmetric)
2. **Monoalphabetic** (Substitution)
3. **Transposition** (Rearrangement)
4. **Vernam** (One-Time Pad)
5. **Playfair** (Digraph Substitution)
6. **Vigenère** (Polyalphabetic)

The system also includes **Base64 encoding** to ensure safe transmission over the network.

---

## Files
* **`server.py`**: The relay application. It listens for incoming files and holds them for the receiver.
* **`client.py`**: The user application. Used by both the Sender (to encrypt/upload) and the Receiver (to download/decrypt).
* **`protocol.py`**: The library containing the math and logic for all 6 encryption algorithms.

---

## Setup & Configuration

### Prerequisites
* Python 3.x installed.
* No external libraries required (uses standard `socket`, `json`, `base64`, `random`).

### Mode A: Simulation (1 Computer)
Use this mode to test everything on a single screen.
1.  Open `client.py`.
2.  Set the IP address to localhost:
    ```python
    SERVER_IP = '127.0.0.1'
    ```

### Mode B: Real Network (3 Computers)
Use this mode for the actual PC-to-PC demonstration.
1.  **PC 1 (Server):** Run `ipconfig` (Windows) or `ifconfig` (Linux/Mac) to find its IPv4 Address (e.g., `192.168.1.15`).
2.  **PC 2 & 3 (Clients):** Open `client.py` and update the variable:
    ```python
    SERVER_IP = '192.168.1.15' # Replace with the actual Server IP
    ```
3.  **Firewall:** On PC 1 (Server), ensure Python is allowed through the Firewall for both Public and Private networks.

---

## Usage Instructions

### Step 1: Start the Server
* Open a terminal/cmd on the **Server PC**.
* Run: `python server.py`
* *Keep this window open. If you close it, the stored data is lost.*

### Step 2: Send a File (Sender)
1.  Create a text file (e.g., `plain.txt`) with your message.
2.  Open a terminal on the **Sender PC**.
3.  Run: `python client.py`
4.  Select **Option 1**.
5.  Enter the filename (`plain.txt`).
6.  Wait for the "Upload Successful" message.
    * *Output:* A file named `EncryptedFile.txt` will be created locally.

### Step 3: Receive the File (Receiver)
1.  Open a terminal on the **Receiver PC**.
2.  Run: `python client.py`
3.  Select **Option 2**.
4.  The system will download the data and reverse the encryption layers.
    * *Output:* A file named `DecryptedText.txt` will be created containing the original message.

---

## Troubleshooting

**Error: "Connection Refused" or "Target machine actively refused it"**
* **Cause:** The Server is not running, or the Firewall is blocking the connection.
* **Fix:** Check that `server.py` is running. Temporarily disable the Firewall on the Server PC to test connectivity.

**Error: "Server is empty"**
* **Cause:** You are trying to download before uploading, or you restarted the Server program (which wipes the memory).
* **Fix:** Restart the Server, run the Sender first, and keep the Server window open while running the Receiver.

**Error: Corrupted/Garbage Decryption**
* **Cause:** Using an old version of `protocol.py` without Base64 safety or small RSA keys.
* **Fix:** Ensure you are using the latest `protocol.py` with `rsa_n = 323` and Base64 encoding.
