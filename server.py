import socket
import json
import threading

HOST = '0.0.0.0' # Listen on all interfaces
PORT = 5000

# Storage for the relay (in memory for simplicity)
stored_data = {
    "ciphertext": None,
    "keys": None
}

def handle_client(conn, addr):
    global stored_data
    print(f"[NEW CONNECTION] {addr} connected.")
    
    try:
        # Receive command
        data = conn.recv(1024 * 1024).decode('utf-8')
        request = json.loads(data)
        
        if request['action'] == 'UPLOAD':
            stored_data['ciphertext'] = request['data']
            stored_data['keys'] = request['keys']
            print(f"[SERVER] Data received and stored from {addr}")
            conn.send("Upload Successful".encode())
            
        elif request['action'] == 'DOWNLOAD':
            if stored_data['ciphertext'] is not None: # <--- CHANGE TO THIS
                payload = json.dumps(stored_data)
                conn.send(payload.encode())
                print(f"[SERVER] Data sent to {addr}")
            else:
                conn.send(json.dumps({"error": "No data found"}).encode())
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()