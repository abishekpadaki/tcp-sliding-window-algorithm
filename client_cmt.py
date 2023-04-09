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

# Function to get the current time in milliseconds


def current_time():
    return int(round(time.time() * 1000))

# Function to transmit packets to the server


def transmit_packets(sock):
    global seq_num
    global terminate_threads
    while not terminate_threads: # Check for termination flag
        if len(sender_window) < window_limit:
            sender_window.append([seq_num, current_time()])
            temp = str(seq_num) + ' '
            msg = temp.encode('utf8')
            sock.sendall(msg)
            print(
                f'\nSequence number "{temp}" sent from the client to the server\n')
            seq_num = (seq_num + pkt_size) % seq_num_wrap_around
            time.sleep(0.0125)

# Function to process acknowledgements received from the server


def process_acknowledgements(sock):
    global terminate_threads
    while not terminate_threads: # Check for termination flag
        data = str(sock.recv(1024).decode('utf8')).strip()
        if not data:
            print("Server closed the connection.")
            terminate_threads = True  # Set termination flag to True
            break
        if data is not None and data != "":
            for d in data.split(' '):
                print(f'\nAcknowledgement number "{d}" received\n')
                if len(sender_window) > 0 and int(d) == sender_window[0][0]:
                    sender_window.popleft()
                    while len(sender_window) != 0 and sender_window[0][0] in extra_acknowledgements:
                        extra_acknowledgements.remove(sender_window[0][0])
                        sender_window.popleft()
                else:
                    extra_acknowledgements.append(int(d))
                    handle_retransmission(sock)
                if len(sender_window) > 0:
                    print(sender_window[0], "\n")
            adjust_window_size(sock)


window_change = 0

# Function to handle retransmission of packets


def handle_retransmission(sock):
    global window_limit
    timeout_duration_ms = 5000
    global window_change
    i = 0
    if len(extra_acknowledgements) >= 20:
        if len(sender_window) > 0:
            msg = (str(sender_window[i][0]) + ' ').encode('utf8')
            sock.sendall(msg)
            window_limit = int(window_limit / 2)
            window_change = 1
            sender_window[i][1] = current_time()
            print(
                f'\nSequence number "{sender_window[i][0]}" retransmitted\n')

# Function to adjust window size based on retransmission events


def adjust_window_size(sock):
    global window_change
    window_timeout_ms = 3000
    max_window_size = 10000
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
    file1.write(str(window_limit) + "," + str(current_time()) + "\n")


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
        console.log(choice.lower())
        sys.exit()
    elif choice.lower() == 'y': 

        # Open file to log window size changes
        file1 = open("windowsize.txt", "a")
        file1.write(str(window_limit) + "," + str(current_time()) + "\n")

        # Receive server response
        while True:
            data = str(s.recv(1024).decode('utf8')).strip()
            if data is not None and data != "":
                print(data, '\n\n')
                break

        # Create and start threads to handle packet transmission and acknowledgement processing
        t1 = threading.Thread(target=transmit_packets, args=(s,))
        t2 = threading.Thread(target=process_acknowledgements, args=(s,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Close the log file
        file1.close()
    else:
        print(f"Incorrect input {choice.lower()}. Please run the program again and enter y or n")
        sys.exit()
