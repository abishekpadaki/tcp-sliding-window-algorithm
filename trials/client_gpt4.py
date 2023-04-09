import socket
import time
import random

def connect_to_server(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    return client_socket

def send_sequence_number(client_socket, seq):
    client_socket.sendall(str(seq).encode())
    data = client_socket.recv(1024)
    if data:
        response = data.decode()
        print(f"Server response: {response}")
        return int(response[3:])
    return None

def main():
    ip = '127.0.0.1'
    port = 12345
    client_socket = connect_to_server(ip, port)

    base = 1
    next_seq_num = 1
    window_size = 4
    max_seq_num = 1000
    buffer = {}
    dropped_packets = set()
    seq_count = 0
    resend_threshold = 10

    while base <= max_seq_num:
        # Send new packets within the window
        while next_seq_num < base + window_size and next_seq_num <= max_seq_num:
            if random.random() > 0.01:  # 1% probability of dropping the packet
                print(f"Sending sequence number: {next_seq_num}")
                buffer[next_seq_num] = send_sequence_number(client_socket, next_seq_num)
            else:
                print(f"Dropping sequence number: {next_seq_num}")
                dropped_packets.add(next_seq_num)
            next_seq_num += 1
            seq_count += 1

            # Retransmit dropped packets after the resend_threshold is reached
            if seq_count >= resend_threshold:
                for dropped_seq in list(dropped_packets):
                    if random.random() > 0.01:  # 1% probability of dropping the packet
                        print(f"Resending sequence number: {dropped_seq}")
                        buffer[dropped_seq] = send_sequence_number(client_socket, dropped_seq)
                        dropped_packets.remove(dropped_seq)
                seq_count = 0

        # Check for received ACKs and update the window
        while base in buffer and buffer[base] is not None:
            print(f"Received ACK for sequence number {base}")
            del buffer[base]
            base += 1

        time.sleep(0.1)

    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()

if __name__ == "__main__":
    main()
