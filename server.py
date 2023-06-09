# ----------------------------------------------------------------------
# Name: Server (Receiver) file of the TCP implementation
# Purpose: CS258 - Coding Project 
# Authors: Abishek Padaki and Jatin Battu
# ----------------------------------------------------------------------



from collections import deque
import time
import sys
import socket
import random

received_pkts = deque([])  # Received packets
pkt_size = 1  # Packet size
wrap_around_limit = 65536  # Sequence number wrap around limit
dropped_packets = {}
curr_drops = []

# Function to get the current time in milliseconds


def elap_time(start_time):
    elapsed_time = time.monotonic() - start_time
    return elapsed_time

# Function to check and maintain the order of received sequence numbers


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

# Function to determine if a packet should be dropped based on a probability


def drop_packet_probability():
    if random.random() < 0.01:
        return False
    else:
        return True


# Main function
if __name__ == "__main__":
    # Create a socket object

    # Open files to log received sequence numbers, dropped packets, goodput, and receiver window size

    # Main loop to process incoming packets
    while True:
            start_time = time.monotonic()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket successfully created")

            # Bind the socket to the specified port
            port = 12345
            s.bind(('', port))
            print("socket binded to %s" % (port))

            # Listen for incoming connections
            s.listen(5)
            print("Socket is listening \n")

            # Accept a connection from a client
            c, addr = s.accept()
            print("Connection established with client %s" % (str(addr)))
            file1 = open("txt_files/seq_number_received.txt", 'a')
            file2 = open("txt_files/seq_number_dropped.txt", 'a')
            file3 = open('txt_files/goodput.txt', 'a')
            file4 = open('txt_files/receiver_window.txt', 'a')
            file5 = open('txt_files/retransmissions.txt', 'a')


            # Receive initial message from client
            hello_msg = c.recv(1024)
            print(hello_msg)

            # Send success message to client
            success_msg = "Success".encode('utf8')
            c.sendall(success_msg)

            # Initialize variables to track packet statistics
            pkts_received = 0
            pkts_sent = 0
            total_pkts = 0

            while True:
                try:
            
                    print(f'\nTotal Packets "{total_pkts}" received\n')
                    data = str(c.recv(1024).decode('utf8')).strip()
                    for d in data.split(' '):
                        if drop_packet_probability():
                            check_sequence_order(int(d))
                            print(f'\nSequence number "{d}" received\n')
                            file1.write(str(d) + ',' + str(elap_time(start_time)) + '\n')
                            file4.write(str(len(received_pkts)) + ',' +
                                        str(elap_time(start_time)) + '\n')
                            msg = (str(d) + ' ').encode('utf8')
                            c.sendall(msg)
                            pkts_received += 1
                            if d in curr_drops:
                                while d in curr_drops:
                                    curr_drops.remove(d)
                                dropped_packets[d] = dropped_packets.get(d,0) + 1
                        else:
                            print(f"Sequence Number {d} Dropped!\n")
                            file2.write(str(d) + ',' + str(elap_time(start_time)) + '\n')
                            if d not in curr_drops:
                                curr_drops.append(d)
                            elif d in curr_drops:
                                dropped_packets[d] = dropped_packets.get(d,0) + 1
                        pkts_sent += 1
                        total_pkts += 1
                        if pkts_received % 1000 == 0:
                            print("Caluclating Good-put...\n")
                            file3.write("Packets Received:" + str(pkts_received) + " Packets Sent: " + str(pkts_sent) +
                                        " Good-put:" + str(pkts_received / pkts_sent) + "\n")
                            print("Packets Received:" + str(pkts_received) + " Packets Sent: " + str(pkts_sent) +
                                        " Good-put:" + str(pkts_received / pkts_sent) + "\n")
                        if total_pkts >= 10000000:
                            print("10000000 Packets received! Closing the Server...\n")
                            print("Caluclating Good-put...\n")
                            file3.write("Packets Received:" + str(pkts_received) + " Packets Sent: " + str(pkts_sent) +
                                        " Good-put:" + str(pkts_received / pkts_sent) + "\n")
                            print("\n Final Packets Received:" + str(pkts_received) + " Final Packets Sent: " + str(pkts_sent) +
                                        " Final Good-put:" + str(pkts_received / pkts_sent) + "\n")
                            
                            for j in dropped_packets:
                                file5.write(str(j)+','+str(dropped_packets[j])+'\n')

                            # Close log files
                            # Close the connection to the client
                            c.close()
                except (ConnectionResetError, socket.error) as e:
                    print(f"[*] Connection reset by client")
                    # Close log files
                    file1.close()
                    file2.close()
                    file3.close()
                    file4.close()
                    file5.close()

                    # Close the connection to the client
                    c.close()
                    break

