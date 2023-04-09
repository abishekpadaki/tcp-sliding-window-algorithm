import socket


# set up socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5300))
server_socket.listen(1)
print('Server Listening')


# accept client connection
client_socket, address = server_socket.accept()
print('Connection from', address)


# receive initial string from client
initial_str = client_socket.recv(1024).decode()
print('Received:', initial_str)


# send connection setup success message to client
success_msg = 'Connection setup success'
client_socket.send(success_msg.encode())


# receive sequence numbers from client and send corresponding ACKs
seq_num = 1
window_size = 4
recv_buffer = []
while True:
    # receive data from client
    data = client_socket.recv(1024)
    if not data:
        break


    # process data and send corresponding ACK
    seq = int(data.decode())
    print('Received Sequence Number:', seq)
    if seq == seq_num:
        recv_buffer.append(seq)


        # send corresponding ACK
        ack_msg = str(seq_num)
        client_socket.send(ack_msg.encode())
        seq_num += 1


        # adjust sliding window
        if len(recv_buffer) >= window_size:
            recv_buffer.pop(0)


client_socket.close()
server_socket.close()