import socket
import zlib

# --- Error Detection Logic (Must match Sender) ---
def calculate_parity(text):
    # simple even parity check for the whole string
    binary_data = ''.join(format(ord(c), '08b') for c in text)
    ones = binary_data.count('1')
    return "1" if ones % 2 != 0 else "0"

def calculate_crc32(text):
    # Using CRC-32 as allowed by instructions
    return hex(zlib.crc32(text.encode()) & 0xffffffff)[2:]

def calculate_2d_parity(text):
    # Simple 8-column matrix parity
    binary_rows = [format(ord(c), '08b') for c in text]
    # Pad if not multiple of 8 (simplified for assignment)
    col_parity = []
    for col_i in range(8):
        bits = [row[col_i] for row in binary_rows]
        col_parity.append("1" if bits.count('1') % 2 != 0 else "0")
    return "".join(col_parity)

# --- Main Receiver Logic ---
def start_receiver():
    host = '127.0.0.1'
    port = 5002

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[*] Client 2 (Receiver) listening on {port}...")

    conn, addr = server_socket.accept()
    print(f"[*] Connection from Server: {addr}")

    while True:
        data_packet = conn.recv(1024).decode()
        if not data_packet:
            break

        print("\n--- Incoming Packet ---")
        print(f"Raw Packet: {data_packet}")
        
        # Expected format: "DATA METHOD|CONTROL_INFO"
        # Example: "HELLO CRC32|a1b2c3d4"
        try:
            # Split logic based on instructions [cite: 58]
            raw_data, rest = data_packet.split(' ')
            method_name, incoming_control = rest.split('|')

            print(f"Received Data: {raw_data}")
            print(f"Method: {method_name}")
            print(f"Sent Check Bits: {incoming_control}")

            # Recalculate
            calculated_control = ""
            if method_name == "Parity":
                calculated_control = calculate_parity(raw_data)
            elif method_name == "CRC32":
                calculated_control = calculate_crc32(raw_data)
            elif method_name == "2DParity":
                calculated_control = calculate_2d_parity(raw_data)
            else:
                calculated_control = "UNKNOWN_METHOD"

            print(f"Computed Check Bits: {calculated_control}")

            # Compare [cite: 65, 73]
            if calculated_control == incoming_control:
                print("Status: DATA CORRECT")
            else:
                print("Status: DATA CORRUPTED")

        except ValueError:
            print("Error: Packet format incorrect.")

    conn.close()

if __name__ == '__main__':
    start_receiver()