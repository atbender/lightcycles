import socket
import sys
import time

client_messages = ('CONNECT', 'DISCONNECT', 'READY', 'TERMINATE', 'TURN')
server_messages = ('WELCOME', 'START', 'CONNECTED', 'DISCONNECTED', 'ISREADY', 'FULL', 'SPAWN', 'TERMINATED', 'VICTORY', 'TURNED')


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

players = []
continue_serving = True
encoding = 'utf-8'


while continue_serving:

    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('new client: ', client_address)
        #players.append(client_address)
        #print(client_address)
        #print(len(players))


        # Receive the data in small chunks and retransmit it
        #chunks = ''
        while True:
            data = connection.recv(2048)
            message = data.decode(encoding)
            print('received {!r}'.format(message))
            if data:
                #chunks = chunks + message
                #print(chunks)
                if message == 'CONNECT':
                    players.append(client_address)
                    print(len(players))

                    #print('sending data back to the client')
                    message = 'WELCOME<{}>'.format(len(players))
                    data = str.encode(message)
                    connection.sendall(data)

            else:
                print('no data from', client_address)
                break
        

    finally:
        

        # Clean up the connection
        connection.close()