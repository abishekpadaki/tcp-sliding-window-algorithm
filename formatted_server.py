from collections import deque
import time
import sys
import socket
import random

received_pkts = deque([])
pkt_size = 5
wrap_around_limit = 65536

def current_time():
    return int(round(time.time() * 1000))

def check_sequence_order(curr_pkt):
    if len(received_pkts) == 0:
        received_pkts.append(curr_pkt)
        return
    for i in range(len(received_pkts)):
        if received_pkts[i] > curr_pkt:
            received_pkts.insert(i, curr_pkt)
            break
    i = 0
    while i < len(received_pkts) - 1:
        if (received_pkts[i] + pkt_size) % wrap_around_limit == received_pkts[i + 1]:
            received_pkts.popleft()
        else:
            break

def drop_packet_probability():
    x = random.randint(1, 100)
    if x == 100:
        return False
    else:
        return True

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    port = 12345
    s.bind(('', port))
    print("socket binded to %s" % (port))
    s.listen(5)
    print("socket is listening \n")
    c, addr = s.accept()
    print("Connection established with client %s" % (str(addr)))
    hello_msg = c.recv(1024)
    print(hello_msg)
    success_msg = "Success".encode('utf8')
    c.sendall(success_msg)
    pkts_received = 0
    pkts_sent = 0
    total_pkts = 0
    file1 = open("seq_number_received.txt", 'a')
    file2 = open("seq_number_dropped.txt", 'a')
    file3 = open('goodput.txt', 'a')
    file4 = open('receiver_window.txt', 'a')

    while True:
        print(f'\nTotal Packets "{total_pkts}" received\n')
        data = str(c.recv(1024).decode('utf8')).strip()
        for d in data.split(' '):
            if drop_packet_probability():
                check_sequence_order(int(d))
                print(f'\nSequence number "{d}" received\n')
                file1.write(str(d) + ',' + str(current_time()) + '\n')
                file4.write(str(len(received_pkts)) + ',' + str(current_time()) + '\n')
                msg = (str(d) + ' ').encode('utf8')
                c.sendall(msg)
                pkts_received += 1
            else:
                file2.write(str(d) + ',' + str(current_time()) + '\n')
            pkts_sent += 1
            total_pkts += 1
            if pkts_received == 1000:
                file3.write(str(pkts_received) + "/" + str(pkts_sent) + "=" + str(pkts_received / pkts_sent) + "\n")
                pkts_sent = 0
                pkts_received = 0
            if total_pkts >= 10000:
                file1.close()
                file2.close()
                file3.close()
                file4.close()
                c.close()
                sys.exit(0)
