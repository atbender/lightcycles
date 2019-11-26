import socket
import sys
import time
from _thread import *

client_messages = ('CONNECT', 'DISCONNECT', 'READY', 'TERMINATE', 'TURN')
server_messages = ('WELCOME', 'START', 'CONNECTED', 'DISCONNECTED', 'ISREADY', 'FULL', 'SPAWN', 'TERMINATED', 'VICTORY', 'TURNED')


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(4)
print('waiting for a connection')

players = []
continue_serving = True
encoding = 'utf-8'

def threaded_client(connection):


    while True:
        try:
            data = connection.recv(2048)
            message = data.decode(encoding)
            print('received {!r}'.format(message))
            if data:
                #chunks = chunks + message
                #print(chunks)
                if message == 'CONNECT':
                    if len(players) >= 4:
                        # send FULL
                        break
                    players.insert(len(players), client_address)
                    print(len(players))

                    print(message, client_address)
                    message = 'WELCOME<{}>'.format(len(players))
                    data = str.encode(message)
                    connection.sendall(data)

                if message == 'DISCONNECT':
                    players.remove(client_address)
                    print(len(players))
                    print(message, client_address)

                

            else:
                print('no data from', client_address)
                break

        except:
            break

    print("lost connection")
    connection.close()


while(True):
    connection, client_address = sock.accept()
    print('new client: ', client_address)
    start_new_thread(threaded_client, (connection,))