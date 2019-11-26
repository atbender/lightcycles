import socket
import sys
import time

encoding = 'utf-8'
client_messages = ('CONNECT', 'DISCONNECT', 'READY', 'TERMINATE', 'TURN')
server_messages = ('WELCOME', 'START', 'CONNECTED', 'DISCONNECTED', 'ISREADY', 'FULL', 'SPAWN', 'TERMINATED', 'VICTORY', 'TURNED')

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)


try:
    
    # Send data
    #message = b'This is the message.  It will be repeated.'
    #print('sending {!r}'.format(message))
    message = 'CONNECT'
    data = str.encode(message)
    sock.sendall(data)

    #chunks = ''

    while True:
        data = sock.recv(2048)
        message = data.decode(encoding)
        print('received {!r}'.format(message))
        if data:
            #chunks = chunks + message
            #print(chunks)

            if (message[0:8] == "WELCOME<") and ((int(message[8:9])) >= 0) and ((int(message[8:9])) <= 3) and (message[9:10]) == ">":
                my_id = int(message[8:9])
                time.sleep(5)
                message = 'DISCONNECT'
                data = str.encode(message)
                sock.sendall(data)
                #break
                #print('sending data back to the client')
                #message = 'WELCOME<{}>'.format(client_address)
                #data = str.encode(message)
                #connection.sendall(data)

        else:
            print('no data from', server_address)
            break
    

finally:
    print('closing socket')
    sock.close()