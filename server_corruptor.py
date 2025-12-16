import socket
import random

# --- Corruption Methods [cite: 36-52] ---
def bit_flip(text):
    # Flip a random bit in the first character
    if not text: return text
    char_list = list(text)
    idx = random.randint(0, len(char_list)-1)
    char_code = ord(char_list[idx])
    # Flip the last bit (XOR 1)
    char_list[idx] = chr(char_code ^ 1)
    return "".join(char_list)

def char_substitution(text):
    if not text: return text
    idx = random.randint(0, len(text)-1)
    return text[:idx] + 'X' + text[idx+1:]

def char_deletion(text):
    if len(text) < 2: return text
    idx = random.randint(0, len(text)-1)
    return text[:idx] + text[idx+1:]

# --- Main Server Logic ---
def start_server():
    # 1. Connect to Client 2 (Receiver)
    receiver_host = '127.0.0.1'
    receiver_port = 5002
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        receiver_socket.connect((receiver_host, receiver_port))
        print(f"[*] Connected to Client 2 on {receiver_port}")
    except:
        print("Error: Could not connect to Client 2. Make sure it is running first.")
        return

    # 2. Listen for Client 1 (Sender)
    listen_host = '127.0.0.1'
    listen_port = 5001
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_host, listen_port))
    server_socket.listen(1)
    print(f"[*] Server (Corruptor) listening for Client 1 on {listen_port}...")

    conn, addr = server_socket.accept()
    print(f"[*] Accepted Client 1: {addr}")

    while True:
        packet = conn.recv(1024).decode()
        if not packet:
            break
        
        print(f"\nReceived from Sender: {packet}")
        
        # Split packet to corrupt only DATA, not control info if possible
        # Format: "DATA METHOD|CONTROL"
        try:
            data_part, meta_part = packet.split(' ', 1)
            
            print("Select Corruption Method:")
            print("1. No Error")
            print("2. Bit Flip")
            print("3. Character Substitution")
            print("4. Character Deletion")
            choice = input("Enter choice (1-4): ")

            corrupted_data = data_part
            if choice == '2':
                corrupted_data = bit_flip(data_part)
            elif choice == '3':
                corrupted_data = char_substitution(data_part)
            elif choice == '4':
                corrupted_data = char_deletion(data_part)
            
            # Reassemble packet
            final_packet = f"{corrupted_data} {meta_part}"
            print(f"Forwarding to Receiver: {final_packet}")
            receiver_socket.send(final_packet.encode())

        except ValueError:
            print("Packet format error, forwarding as is...")
            receiver_socket.send(packet.encode())

    conn.close()
    receiver_socket.close()

if __name__ == '__main__':
    start_server()