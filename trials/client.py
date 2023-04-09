import socket


# set up socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5300))
client_port = client_socket.getsockname()[1]
print("Client port number:", client_port)


# send initial string to server
initial_str = 'network'
client_socket.send(initial_str.encode())


# receive connection setup success message from server
success_msg = client_socket.recv(1024).decode()
print('Received:', success_msg)


# send sequence numbers to server
seq_num = 1
window_size = 4
while seq_num <= 10000:
    for i in range(window_size):
        # send individual sequence numbers to server
        client_socket.send(str(seq_num).encode())


        # receive corresponding ACK from server
        ack = client_socket.recv(1024).decode()
        print('Received ACK:', ack)


        # adjust sliding window
        seq_num += 1


client_socket.close()
