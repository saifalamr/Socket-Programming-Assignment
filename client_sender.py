import socket
import zlib

# --- Control Info Generation [cite: 13-27] ---
def calculate_parity(text):
    # Odd/Even parity based on total count of 1s
    binary_data = ''.join(format(ord(c), '08b') for c in text)
    ones = binary_data.count('1')
    return "1" if ones % 2 != 0 else "0"

def calculate_crc32(text):
    # Returns hex value of CRC
    return hex(zlib.crc32(text.encode()) & 0xffffffff)[2:]

def calculate_2d_parity(text):
    binary_rows = [format(ord(c), '08b') for c in text]
    col_parity = []
    for col_i in range(8):
        bits = [row[col_i] for row in binary_rows]
        col_parity.append("1" if bits.count('1') % 2 != 0 else "0")
    return "".join(col_parity)

# --- Main Sender Logic ---
def start_sender():
    host = '127.0.0.1'
    port = 5001  # Connects to Server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"[*] Connected to Server on {port}")
    except:
        print("Error: Could not connect to Server. Ensure it is running.")
        return

    while True:
        text = input("\nEnter text to send (or 'exit'): ")
        if text == 'exit': break
        
        print("Choose Method:")
        print("1. Parity")
        print("2. CRC32")
        print("3. 2D Parity")
        choice = input("Choice: ")

        method_str = ""
        control_info = ""

        if choice == '1':
            method_str = "Parity"
            control_info = calculate_parity(text)
        elif choice == '2':
            method_str = "CRC32"
            control_info = calculate_crc32(text)
        elif choice == '3':
            method_str = "2DParity"
            control_info = calculate_2d_parity(text)
        else:
            print("Invalid choice.")
            continue

        # Format: DATA METHOD|CONTROL [cite: 29]
        packet = f"{text} {method_str}|{control_info}"
        client_socket.send(packet.encode())
        print(f"Sent: {packet}")

    client_socket.close()

if __name__ == '__main__':
    start_sender()