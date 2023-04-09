from collections import deque
import time
import sys
# Import socket module
import socket    
import random
received_packets=deque([]) #dequeue for the received packets
packet_size=5 #setting packet size to 5
wrap_around=65536 # Setting Wrap around to 2^16

def sys_time(): #calculating the system time
    return int(round(time.time()*1000))

def sequence_check(current_packet): #checking if the packets are arriving in order
    if len(received_packets)==0: #if the queue is empty, add the current packet
        received_packets.append(current_packet)
        return
    for i in range(len(received_packets)):
        if received_packets[i] > current_packet:
            received_packets.insert(i,current_packet)
            break
    i=0
    while i < len(received_packets)-1:
        if (received_packets[i]+packet_size)%wrap_around==received_packets[i+1]: #applying the wraparound
            received_packets.popleft()
        else:
            break

def checkIfDropped(): #randomized dropping of 1 packet for every 100 packets (1%)
    x=random.randint(1,100)
    if x==100:
        return False
    else:
        return True 

if __name__=="__main__":
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #initializing the socket
    print ("Socket successfully created")
    port=12345 #reserving a port
    s.bind(('',port))		
    print ("socket binded to %s" %(port))
    s.listen(5)	#put the socket into listening mode
    print ("socket is listening \n")		
    c,addr=s.accept() #connecting the the client
    print("Connection established with client %s" %(str(addr)))
    hello_msg=c.recv(1024) #receive message from the client
    print(hello_msg) #print the received message
    success_message="Success".encode('utf8')
    c.sendall(success_message) #send a success message
    no_of_packets_received=0
    no_of_packets_sent=0
    total_packets=0
    #open the files to write the data into for getting the graphs
    file1=open("seq_number_received.txt",'a')
    file2=open("seq_number_dropped.txt",'a')
    file3=open('goodput.txt','a')
    file4=open('receiver_window.txt','a')

    while True:
    # Establish connection with client.	
        print(f'\nTotal Packets "{total_packets}" received\n')
        data=str(c.recv(1024).decode('utf8')).strip()
        for d in data.split(' '):
            if checkIfDropped(): #first check if the packet has been dropped
                sequence_check(int(d)) #call the sequence order checking function
                print(f'\nSequence number "{d}" received\n')
                file1.write(str(d)+','+str(sys_time())+'\n') #writing the time at which the packet was received
                file4.write(str(len(received_packets))+','+str(sys_time())+'\n') #writing the time at which the packet was received
                msg=(str(d)+' ').encode('utf8')
                c.sendall(msg)
                no_of_packets_received+=1 #increment the number of received packets
            else:
                file2.write(str(d)+','+str(sys_time())+'\n')
            no_of_packets_sent+=1
            total_packets+=1
            if no_of_packets_received==1000: #calculating goodput after every 1000 packets received
                file3.write(str(no_of_packets_received)+"/"+str(no_of_packets_sent)+"="+str(no_of_packets_received/no_of_packets_sent)+"\n")
                no_of_packets_sent=0
                no_of_packets_received=0
            if total_packets>=100000: #stop the socket after 10 million packets
                file1.close()
                file2.close()
                file3.close()
                file4.close()
                c.close()
                sys.exit(0)
