from collections import deque
import time
#Import socket module
import socket    
import threading

client_window=deque([]) #client window is stored as a deque to facilitate pushing and popping from both ends
seq_counter=0 #the sequence numbers that we are sening to the server
window_size=15 #Setting window size to 3
packet_size=5 #Size of each packet
extra_ack=[]
wrap_around=65536 # Setting Wrap around to 2^16

#function to generate the system time
def sys_time():
    return int(round(time.time()* 1000))

def sendPackets(sock):
    global seq_counter
    while 1:
        if len(client_window) < window_size:
            client_window.append([seq_counter, sys_time()]) #add the sequence number and the time at which it was sent
            temp=str(seq_counter)+' '
            msg=temp.encode('utf8')
            sock.sendall(msg) #send it to the server
            print(f'\nSequence number"{temp}" sent from the client to the server\n') #print it for the user to see
            seq_counter=(seq_counter+packet_size)%wrap_around #wraparound after 2^16 packets
            time.sleep(0.0125) #add a sleep time for letting the server receive the packet since we use threading


# def timer_window_resize(sock):
#     pass


def processAck(sock): #function for processing the acknowledgement
    while 1:
        data=str(sock.recv(1024).decode('utf8')).strip() #receive acknowledgement from the server
        if data is not None and data != "":
            for d in data.split(' '):
                print(f'\nAcknowledgement number "{d}" received\n') #print the acknowledgement that has been received
                if len(client_window)>0 and int(d) == client_window[0][0]: #check if the acknowledgement received is for the sent packet
                    client_window.popleft()
                    while len(client_window)!=0 and client_window[0][0] in extra_ack:
                        extra_ack.remove(client_window[0][0])
                        client_window.popleft()
                else:
                    extra_ack.append(int(d))
                    retransmit(sock)
                if len(client_window)>0:
                    print(client_window[0],"\n")
            window_resize(sock) #change window size

window_increment=0

def retransmit(sock):
    global window_size
    timeout_ms=5000
    global window_increment
    i = 0
    if len(extra_ack)>=20: #checking for 20 out of order packets
        if len(client_window)>0:
            msg=(str(client_window[i][0])+' ').encode('utf8')
            sock.sendall(msg)
            window_size=int(window_size/2) #divide thw window size by half
            window_increment=1
            client_window[i][1] = sys_time() #update the time to the current time
            print(f'\nSequence number "{client_window[i][0]}" retransmit from the client to the server\n')


def window_resize(sock):
    global window_increment
    window_timeout_ms=3000
    maxsize=10000
    global window_size
    temp = window_size
    if window_increment==0:
        new_window_size=window_size*2 #doubling the window size if the acknowledgment is in order
    else:
        new_window_size=window_size+1 #else incrementing it by 1
    
    if new_window_size>=maxsize:
        window_size=maxsize
    elif new_window_size<=0:
        window_size=1
    else:
        window_size=new_window_size
    print(f'\n window size changed from {temp} to {window_size}') #write it to a file to get the graph
    file1.write(str(window_size)+","+str(sys_time())+"\n")


if __name__ == "__main__":
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port=12345
    server_ip_addr='127.0.0.1'  #set the IP address of the server
    s.connect((server_ip_addr, port)) #establish connection
    print(f'\n Connected to Server with IP Address: {server_ip_addr} and Port: {port}')
    msg=("Hello Server").encode('utf8') #send hello
    s.sendall(msg)
    file1 = open("windowsize.txt", "a")  # append mode
    file1.write(str(window_size)+","+str(sys_time())+"\n")
    while 1:
        data=str(s.recv(1024).decode('utf8')).strip()
        if data is not None and data != "":
            print(data,'\n\n')
            break
    t1 = threading.Thread(target=sendPackets, args=(s,)) #run send packets and process acknowledgement function using multi threading
    t2 = threading.Thread(target=processAck, args=(s,))
    t1.start() #starting thread 1
    t2.start() #starting thread 2
    t1.join() #wait until thread 1 is completely executed
    t2.join() #wait until thread 2 is completely executed
    file1.close()