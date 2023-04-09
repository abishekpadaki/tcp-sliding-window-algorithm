import socket

# defining the server's IP address and port number
server_ip_address = '127.0.0.1'
server_port = 9999

# creating a TCP socket and connecting to the server's IP address and port number
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip_address, server_port))

# sending initial string to the server
initial_string = 'network'
client_socket.send(initial_string.encode())

# receiving connection setup success message from the server
connection_setup_message = client_socket.recv(1024).decode()
print(connection_setup_message)

# sending packets and acknowledging individual packets
max_sequence_number = 2**16 - 1 # as maximum sequence number should be limited to 216
current_sequence_number = 0
while current_sequence_number < 10000000:
    # sending packet with current sequence number
    packet = current_sequence_number.to_bytes(2, byteorder='big')
    client_socket.send(packet)
    
    # receiving ACK for the sent packet
    ack_packet = client_socket.recv(1024)
    ack_sequence_number = int.from_bytes(ack_packet, byteorder='big')
    
    # checking if received ACK number is expected
    if ack_sequence_number == current_sequence_number:
        # adjusting sequence number by incrementing it
        current_sequence_number += 1
    else:
        # in case of missing sequence number, resending the packet
        pass

# closing client socket
client_socket.close()
