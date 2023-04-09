import socket

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f"Server listening on {ip}:{port}")
    return server_socket

def process_data(data, expected_seq, missing_seqs):
    seq = int(data)
    if seq == expected_seq:
        expected_seq += 1
    elif seq > expected_seq:
        missing_seqs.update(range(expected_seq, seq))
        expected_seq = seq + 1

    return expected_seq, missing_seqs

def main():
    ip = '127.0.0.1'
    port = 12345
    server_socket = start_server(ip, port)

    expected_seq = 1
    missing_seqs = set()
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        seq = data.decode()
        print(f"Received sequence number: {seq}")
        expected_seq, missing_seqs = process_data(seq, expected_seq, missing_seqs)
        client_socket.sendall(f"ACK{seq}".encode())

    print("Missing sequence numbers:", missing_seqs)
    client_socket.close()

if __name__ == "__main__":
    main()
