import socket
import random
import time


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

all_drops = []
all_sent = []
window_size_changes = []


# send sequence numbers to server
round_counter = 1
total_packets = 1
seq_num = 1
window_size = 4
window = []
missing_packets = []
max_packets = 100000
max_seq_num = 2**16
start_time = time.time()

def send_from_window():
        global window
        global seq_num
        global round_counter
        global missing_packets
        print("Sliding Window Threshold reached, Sending a packet!")
        send_seq, send_rc = window[0].split(',') 
        client_socket.send((f'{send_seq},{send_rc}').encode())
        global total_packets
        total_packets += 1
        print(f'Sent Sequence Number: {send_seq},{send_rc}')
        all_sent.append(send_seq)
        ack = client_socket.recv(1024).decode()
        window.remove(ack)
        if ack in missing_packets:
            missing_packets.remove(ack)

def retransmit():
    global window
    global missing_packets
    #remove all existing window items
    for i in missing_packets:
        if random.random() < 0.01:
                continue
        else:
            if (len(window) < window_size):
                re_seq_number, re_round_count = i.split(',')
                window.append(f'{re_seq_number},{re_round_count}')
                
            else:
                send_from_window()                
                re_seq_number, re_round_count = i.split(',')
                window.append(f'{re_seq_number},{re_round_count}')
        print('Done Retransmitting')


while total_packets <= max_packets:

    

    # periodic retransmission
    # if (total_packets % 505 == 0):
    #     retransmit()

    prev_window_size = len(window)

    # send individual sequence numbers to server with a 1% probability of dropping the packet


    # if random.random() < 0.01:
    #     missing_packets.append(f'{seq_num},{round_counter}')
    #     print("Dropped Sequence Number: ", seq_num)
       
    #     # Code to be timed
    #     end_time = time.time()
    #     elapsed_time = end_time - start_time
    #     all_drops.append(f'{seq_num}\t{elapsed_time}')
    #     if (seq_num >= max_seq_num + 1):
    #         total_packets += 1
    #         round_counter += 1
    #         seq_num = 1
    #         continue
    #     else:
    #         seq_num += 1
    #         total_packets += 1
    #         continue


    # If window size is lesser is max size, append till window full  
    if (len(window) < window_size):
        window.append(f'{seq_num},{round_counter}')
    else:
        send_from_window()
        continue
    
    seq_num += 1
    
    if (seq_num >= max_seq_num + 1):
                round_counter += 1
                seq_num = 1

                

    # receive corresponding ACK from server
    
    #print('Received ACK:', ack)




client_socket.close()


# print missing packets at the end of execution
if missing_packets:
    print(f"Missing packets: {missing_packets}")
    print(len(missing_packets))
else:
    print("No packets were lost.")

print(f'Total Number of Packets Sent (incl. dropped): {len(all_sent) + len(missing_packets)}')
print(f"Number of Packets Sent Successfully: {len(all_sent)}")

with open('drop_time.txt', 'w') as f:
    for item in all_drops:
        f.write("%s\n" % item)

with open('window_size_changes_client.txt', 'w') as f:
    for item in window_size_changes:
        f.write("%s\n" % item)
