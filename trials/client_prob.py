import socket
import random


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
missing_packets = []


def retransmit(dropped_packets):
    d_packets = dropped_packets
    for i in d_packets:
        if random.random() < 0.01:
            print("Dropped Sequence Number: ",i)
            continue
        client_socket.send(str(i).encode())
        print('Sent Sequence Number: ', i)
                 # receive corresponding ACK from server
        ack = client_socket.recv(1024).decode()
        d_packets.remove(ack)
    return d_packets



while seq_num <= 10000:
    
    for i in range(window_size):
        # send individual sequence numbers to server with a 1% probability of dropping the packet
        if random.random() < 0.01:
            missing_packets.append(seq_num)
            # print("Dropped Sequence Number: ",seq_num)
            seq_num += 1
            continue


        client_socket.send(str(seq_num).encode())
        # print('Sent Sequence Number: ', seq_num)
        # receive corresponding ACK from server
        ack = client_socket.recv(1024).decode()
        #print('Received ACK:', ack)


        # adjust sliding window
        seq_num += 1
        if seq_num % 150 == 0:
            print('in')
            new_missing_packets = retransmit(missing_packets)
            missing_packets = new_missing_packets


client_socket.close()


# print missing packets at the end of execution
if missing_packets:
    print(f"Missing packets: {missing_packets}")
    print(len(missing_packets))
else:
    print("No packets were lost.")
