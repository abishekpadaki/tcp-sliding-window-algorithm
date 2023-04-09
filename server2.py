import socket

# defining the server's IP address and port number
server_ip_address = '127.0.0.1'
server_port = 9999

# creating a TCP socket and binding it to the server's IP address and port number
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip_address, server_port))

# setting up the server to listen to incoming connections
server_socket.listen()

print('Server is ready to receive...')

# accepting incoming connections
client_socket, client_address = server_socket.accept()

# receiving initial string from the client
initial_string = client_socket.recv(1024).decode()
print('Received initial string:', initial_string)

# sending connection setup success message to the client
client_socket.send('Connection setup success'.encode())

# receiving packets from the client and sending corresponding ACK numbers
expected_sequence_number = 0
while expected_sequence_number < 10000000:
    # receiving packet from the client
    packet = client_socket.recv(1024)
    
    if not packet:
        break
        
    # getting sequence number from the packet
    sequence_number = int.from_bytes(packet, byteorder='big')
    
    # checking if sequence number is expected
    if sequence_number == expected_sequence_number:
        # sending corresponding ACK number to the client
        client_socket.send(packet)
        
        # incrementing expected sequence number
        expected_sequence_number += 1
        
# closing client socket
client_socket.close()

# closing server socket
server_socket.close()

