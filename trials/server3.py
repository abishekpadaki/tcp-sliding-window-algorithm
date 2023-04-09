import socket
import time

def elapsed_time(start):
        end_time = time.time()
        return (end_time - start)


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
round_counter = 1
total_received = 0
window_size = 4
recv_buffer = []
missing_packets = []
goodput_tracker = []
max_seq_num = 2**16
start_time = time.time()
all_seq_rcv = []

while True:
    # receive data from client
    data = client_socket.recv(1024)
    if not data:
        break

    # process data and send corresponding ACK
    rcvseq = str(data.decode())
    seq, rc = rcvseq.split(',')
    seq = int(seq)
    rc = int(rc)
    print(f'Received Sequence Number: {seq},{rc}')
    all_seq_rcv.append(f'{seq}\t{elapsed_time(start_time)}')
    recv_buffer.append(f'{seq},{rc}')

    # calculating goodput
    if (seq_num % 1000 == 0):
        t_sent = total_received + len(missing_packets)
        goodput = total_received / t_sent
        goodput_tracker.append(goodput)

    if (f'{seq},{rc}' in missing_packets):
        if (len(recv_buffer) < window_size):
            ack_msg = str(f'{seq},{rc}')
            client_socket.send(ack_msg.encode())
            missing_packets.remove(f'{seq},{rc}')
            recv_buffer.remove(f'{seq},{rc}')
            total_received += 1
            continue

    # send corresponding ACK

    if (seq == seq_num and rc == round_counter and len(recv_buffer) < window_size):
        ack_msg = str(f'{seq},{rc}')
        client_socket.send(ack_msg.encode())
        recv_buffer.remove(f'{seq},{rc}')

    if (seq > seq_num and rc == round_counter and len(recv_buffer) < window_size):
        diff = seq-seq_num
        for i in range(diff):
            missing_packets.append(f'{seq_num},{round_counter}')
            seq_num += 1
        seq_num = seq
        ack_msg = str(f'{seq_num},{round_counter}')
        client_socket.send(ack_msg.encode())
        recv_buffer.remove(f'{seq_num},{round_counter}')
    if (rc != round_counter and round_counter > rc and seq < seq_num):
        diff = max_seq_num - seq_num
        for i in range(diff):
            missing_packets.append(f'{seq_num},{round_counter}')
            seq_num += 1
        seq_num = seq
        round_counter = rc
        ack_msg = str(f'{seq_num},{round_counter}')
        client_socket.send(ack_msg.encode())
        recv_buffer.remove(f'{seq_num},{round_counter}')

    seq_num += 1
    total_received += 1
    # wrap-around
    if seq_num >= max_seq_num + 1:
        round_counter += 1
        seq_num = 1


# close connections
client_socket.close()
server_socket.close()


# print missing packets
if missing_packets:
    print(f"Missing packets: {missing_packets}")
    print(len(missing_packets))
else:
    print("No packets were lost.")

print(f'Total Number of Packets Sent (incl. dropped): {total_received + len(missing_packets)}')
print(f'Total Number of Packets Received Successfully: {total_received}')


# print(f"Periodic Good-Put: {goodput_tracker}")

with open('receive_time.txt', 'w') as f:
    for item in all_seq_rcv:
        f.write("%s\n" % item)
