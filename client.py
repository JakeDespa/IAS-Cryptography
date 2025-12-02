import socket
import json
import os
from protocol import CryptoPipeline

SERVER_IP = '127.0.0.1' # Change to Server IP if on different PCs
PORT = 5000

def sender_mode():
    print("\n--- SENDER MODE ---")
    filename = input("Enter filename to upload (e.g., plain.txt): ")
    
    if not os.path.exists(filename):
        print("File not found.")
        return

    # 1. Read File
    with open(filename, 'r', encoding='utf-8') as f:
        plaintext = f.read()

    # 2. Apply Pipeline (Flowchart: Upload -> Generate Keys -> Apply Ciphers)
    cp = CryptoPipeline()
    print("Applying: RSA -> Mono -> Transp -> Vernam -> Playfair -> Vigenere...")
    ciphertext, keys, original_hash = cp.full_encryption_pipeline(plaintext)
    
    # 3. Send to Server
    payload = {
        "action": "UPLOAD",
        "data": ciphertext,
        "keys": keys, # Sending keys to server to simulate passing them to receiver
        "hash": original_hash
    }
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    client.send(json.dumps(payload).encode('utf-8'))
    response = client.recv(1024).decode()
    print(f"Server Response: {response}")
    
    # Save local copy of encrypted file as per flowchart
    with open("EncryptedFile.txt", "w", encoding='utf-8') as f:
        f.write(ciphertext)
    print("Saved EncryptedFile.txt locally.")

def receiver_mode():
    print("\n--- RECEIVER MODE ---")
    input("Press Enter to connect to server and download...")
    
    # 1. Download from Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    req = {"action": "DOWNLOAD"}
    client.send(json.dumps(req).encode('utf-8'))
    
    data = client.recv(1024 * 1024).decode()
    try:
        package = json.loads(data)
        if "error" in package:
            print("Server is empty.")
            return
            
        ciphertext = package['ciphertext']
        keys = package['keys']
        original_hash = package['hash']
        
        print("File downloaded.")
        
        # 2. Decrypt Pipeline (Flowchart: Reverse RSA... actually Reverse Order)
        cp = CryptoPipeline()
        print("Decrypting layers...")
        decrypted_text = cp.full_decryption_pipeline(ciphertext, keys, original_hash)
        
        # 3. Save Output
        with open("DecryptedText.txt", "w", encoding='utf-8') as f:
            f.write(decrypted_text)
        print(f"Decryption Complete! Content: {decrypted_text}")
        
    except json.JSONDecodeError:
        print("Failed to parse data.")

def main():
    print("1. Encrypt & Upload (Sender)")
    print("2. Download & Decrypt (Receiver)")
    choice = input("Select Process: ")
    
    if choice == '1':
        sender_mode()
    elif choice == '2':
        receiver_mode()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()