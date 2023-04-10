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
window_limit = 4  # Initial window size
pkt_size = 1  # Packet size
extra_acknowledgements = []  # Extra acknowledgements
seq_num_wrap_around = 65536  # Sequence number wrap around limit
terminate_threads = False  # Global flag to signal threads to terminate
start_time = time.monotonic()
terminate_event = threading.Event()
data_lock = threading.Lock()
ret = {}
sent_packets = {}  # Store the status of sent packets
window_change = 0
duplicate_ack_count = {}




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
            window_not_full = len(sender_window) < window_limit
        if window_not_full:
            sent_packets[seq_num] = False  # Mark the packet as not acknowledged
            sender_window.append([seq_num, elap_time(start_time)])
            temp = str(seq_num) + ' '
            seq_num = (seq_num + pkt_size) % seq_num_wrap_around
            msg = temp.encode('utf8')
            sock.sendall(msg)
            print(f'\nSequence number "{temp}" sent from the client to the server\n')
            time.sleep(0.0125)
                # Check if it's time to retransmit dropped packets
            if seq_num % 100 == 0:
                retransmit_dropped_packets(sock)
        else:
            temp = None
            print('\nSender Window Full\n')
            
            
# Function to process acknowledgements received from the server

# New function to retransmit dropped packets after every 100 sequence numbers
def retransmit_dropped_packets(sock):
    global sent_packets
    global ret
    global window_change
    global window_limit
    global extra_acknowledgements

    for seq_num, acknowledged in sent_packets.items():
        if not acknowledged:
            msg = (str(seq_num) + ' ').encode('utf8')
            sock.sendall(msg)
            print(f'\nSequence number "{seq_num}" retransmitted\n')
            ret[str(seq_num)] = ret.get(str(seq_num), 0) + 1

            for i, pkt in enumerate(sender_window):
                if pkt[0] == seq_num:
                    del sender_window[i]
                    break
            window_limit = max(int(window_limit / 2), 1)
            window_change = 1
            adjust_window_size()

    # Clear the sent_packets dictionary to avoid retransmitting the same packets again
    sent_packets.clear()
    # window_limit = max(int(window_limit / 2), 1)
    # window_change = 1

def process_acknowledgements(sock):
    global terminate_event
    global window_limit
    global window_change
    
    while not terminate_event.is_set(): # Check for termination flag
        data = str(sock.recv(1024).decode('utf8')).strip()
        if not data:
            print("Server closed the connection.")
            terminate_event.set()  # Signal termination
            break
        if data and data != "":
            with data_lock:
                for d in data.split(' '):
                    print(f'\nAcknowledgement number "{d}" received\n')
                    # Update the status of the acknowledged packet
                    seq_ack = int(d)
                    # Update the status of the acknowledged packet
                    sent_packets[seq_ack] = True
                    window_change = 0
                    adjust_window_size()

                    # if seq_ack in duplicate_ack_count:
                    #     duplicate_ack_count[seq_ack] += 1
                    #     if duplicate_ack_count[seq_ack] >=2:
                    #         # Apply congestion control
                            
                    #         print(f'Window limit reduced to {window_limit} due to congestion')
                    #         duplicate_ack_count[seq_ack] = 0  # Reset the count for this acknowledgement
                    # else:
                    #     duplicate_ack_count[seq_ack] = 1


                    while len(sender_window) > 0 and sender_window[0][0] == seq_ack:
                        sender_window.popleft()
                        if len(sender_window) > 0:
                            seq_ack = sender_window[0][0]
                   
                



# Function to handle retransmission of packets


# def handle_retransmission(sock):
#     global start_time
#     global window_limit
#     global window_change
#     global ret
#     i = 0
#     if len(extra_acknowledgements) >= 20:
#         if len(sender_window) > 0:
#             msg = (str(sender_window[i][0]) + ' ').encode('utf8')
#             sock.sendall(msg)
#             window_limit = int(window_limit / 2)
#             window_change = 1
#             sender_window[i][1] = elap_time(start_time)
#             print(
#                 f'\nSequence number "{sender_window[i][0]}" retransmitted\n')
#             ret[str(sender_window[i][0])] = ret.get(str(sender_window[i][0]),0) + 1

# Function to adjust window size based on retransmission events


def adjust_window_size():
    global window_change
    global start_time
    max_window_size = 100000
    global window_limit
    global sender_window
    old_window_size = window_limit
    unacknowledged_packets = len(sender_window)

    if unacknowledged_packets > 0:
        if window_change == 0:
            new_window_limit = window_limit * 2
        else:
            new_window_limit = window_limit + 1
    else:
        new_window_limit = window_limit

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

    choice = input("Are you ready to begin sending packets? (Y/N):")
    if choice.lower() == 'n':
        print(choice.lower())
        sys.exit()
    elif choice.lower() == 'y': 

        # Open file to log window size changes
        file1 = open("txt_files/windowsize.txt", "a")
        file1.write(str(window_limit) + "," + str(elap_time(start_time)) + "\n")

        file2 = open("txt_files/re.txt", "a")
        

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
            print(f"Error: {e}")
            terminate_event.set()  # Signal termination
            t1.join()
            t2.join()
        finally:
         # Close the log file
            file1.close()
            for value in ret:
                file2.write(f'{value},{ret[value]}\n')
            file2.close()
    else:
        print(f"Incorrect input {choice.lower()}. Please run the program again and enter y or n")
        sys.exit()
