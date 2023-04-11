# ----------------------------------------------------------------------
# Name: Client (Sender) file of the TCP implementation
# Purpose: CS258 - Coding Project 
# Authors: Abishek Padaki and Jatin Battu
# ----------------------------------------------------------------------

from collections import deque
import time
import socket
import threading
import sys

# Initialize global variables
sender_window = deque([])  # Sliding window
seq_num = 0  # Sequence number
window_limit = 15  # Initial window size
pkt_size = 1  # Packet size
extra_acknowledgements = []  # Extra acknowledgements
seq_num_wrap_around = 65536  # Sequence number wrap around limit
terminate_threads = False  # Global flag to signal threads to terminate
start_time = time.monotonic()
terminate_event = threading.Event()
data_lock = threading.Lock()


# Function to get the current time in milliseconds


def elap_time(start_time):
    elapsed_time = time.monotonic() - start_time
    return elapsed_time

# Function to transmit packets to the server


def transmit_packets(sock):
    global seq_num
    global start_time
    while not terminate_event.is_set():
        with data_lock: # Check for termination flag
            if len(sender_window) < window_limit:
                sender_window.append([seq_num, elap_time(start_time)])
                temp = str(seq_num) + ' '
                seq_num = (seq_num + pkt_size) % seq_num_wrap_around
                msg = temp.encode('utf8')
                sock.sendall(msg)
                print(f'\nSequence number "{temp}" sent from the client to the server\n')
                # time.sleep(0.0125)
            else:
                temp = None
                print('\nSender Window Full\n')
# Function to process acknowledgements received from the server


def process_acknowledgements(sock):
    global window_change
    global terminate_event
    while not terminate_event.is_set(): # Check for termination flag
        data = str(sock.recv(1024).decode('utf8')).strip()
        if not data:
            print("Server closed the connection.")
            terminate_event.set()  # Signal termination
            break
        if data is not None and data != "":
            with data_lock:
                for d in data.split(' '):
                    print(f'\nAcknowledgement number "{d}" received\n')
                    if len(sender_window) > 0 and int(d) == sender_window[0][0]:
                        sender_window.popleft()
                        while len(sender_window) != 0 and sender_window[0][0] in extra_acknowledgements:
                            extra_acknowledgements.remove(sender_window[0][0])
                            sender_window.popleft()
                        window_change = 0
                    else:
                        extra_acknowledgements.append(int(d))
                        handle_retransmission(sock)
                    if len(sender_window) > 0:
                        print(sender_window[0], "\n")
                    adjust_window_size(sock)


window_change = 0

# Function to handle retransmission of packets


def handle_retransmission(sock):
    global start_time
    global window_limit
    global window_change
    i = 0
    if len(extra_acknowledgements) >= 20:
        if len(sender_window) > 0:
            msg = (str(sender_window[i][0]) + ' ').encode('utf8')
            sock.sendall(msg)
            window_limit = int(window_limit / 2)
            window_change = 1
            sender_window[i][1] = elap_time(start_time)
            print(
                f'\nSequence number "{sender_window[i][0]}" retransmitted\n')

# Function to adjust window size based on retransmission events


def adjust_window_size(sock):
    global window_change
    global start_time
    max_window_size = 100000
    global window_limit
    old_window_size = window_limit
    if window_change == 0:
        new_window_limit = window_limit * 2
    else:
        new_window_limit = window_limit + 1

    if new_window_limit >= max_window_size:
        window_limit = max_window_size
    elif new_window_limit <= 0:
        window_limit = 1
    else:
        window_limit = new_window_limit
    print(f'\n window size changed from {old_window_size} to {window_limit}')
    file1.write(str(window_limit) + "," + str(elap_time(start_time)) + "\n")


# Main function
if __name__ == "__main__":
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345  # Server port
    server_ip_address = '127.0.0.1'  # Server IP address

    # Connect to the server
    s.connect((server_ip_address, port))
    print(
        f'\n Connected to Server with IP Address: {server_ip_address} and Port: {port}')

    # Send initial message to server
    msg = ("Network").encode('utf8')
    s.sendall(msg)

        # Open file to log window size changes
    file1 = open("txt_files/windowsize.txt", "a")
    file1.write(str(window_limit) + "," + str(elap_time(start_time)) + "\n")

        # Receive server response
    while True:
        data = str(s.recv(1024).decode('utf8')).strip()
        if data is not None and data != "":
            print(data, '\n\n')
            break
    try:
            # Create and start threads to handle packet transmission and acknowledgement processing
        t1 = threading.Thread(target=transmit_packets, args=(s,))
        t2 = threading.Thread(target=process_acknowledgements, args=(s,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except:
        print(f"Error. Terminating.")
        terminate_event.set()  # Signal termination
        t1.join()
        t2.join()
    finally:
         # Close the log file
        file1.close()
   
