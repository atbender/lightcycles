import socket
import sys
import time
from _thread import *

client_messages = ('CONNECT', 'DISCONNECT', 'READY', 'TERMINATE', 'TURN')
server_messages = ('WELCOME', 'START', 'CONNECTED', 'DISCONNECTED', 'ISREADY', 'FULL', 'SPAWN', 'TERMINATED', 'VICTORY', 'TURNED')


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10001)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(4)
sock.setblocking(False)
print('waiting for a connection')

players = ['empty', 'empty', 'empty', 'empty']
clients = []
global player_number
player_number = 0

def addPlayer(address):
    for i in range(4):
        print('i =', i)
        if(players[i] == 'empty'):
            players[i] = address
            print(players)
            global player_number
            player_number = player_number + 1
            print(player_number)
            return i

    return False

def removePlayer(address):
    try:
        players[players.index(address)] = 'empty'
        print(players)
        player_number -= 1
    except:
        pass


continue_serving = True
encoding = 'utf-8'


while(True):
    try:
        connection, client_address = sock.accept()
        clients.append((connection, client_address))
        print('new client: ', client_address)
        print(clients)
    
    except BlockingIOError:
        for connection, client_address in clients:
            print('serving ', client_address)
            try:
                data = connection.recv(2048)
                message = data.decode(encoding)
                print('received {!r}'.format(message))
                if data:
                    #chunks = chunks + message
                    #print(chunks)
                    if message == 'CONNECT':
                        print(player_number)
                        if player_number >= 4:
                            # send FULL
                            print('full')
                            removePlayer(client_address)
                            clients.remove((connection, client_address))
                            print("lost connection")
                            connection.close()
                            exit()

                        player_id = 0
                        player_id = addPlayer(client_address)
                        #print('aaaaaaaaaaaaaaaaaa')
                        print(player_id)
                        print(message, client_address)
                        message = 'WELCOME<{}>'.format(player_id)
                        data = str.encode(message)
                        connection.sendall(data)

                    if message == 'DISCONNECT':
                        removePlayer(client_address)
                        print(player_number)
                        print(message, client_address)
                        clients.remove((connection, client_address))
                        print("lost connection")
                        connection.close()
                        exit()

                    if message[0:5] == "TURN<":
                        # get id
                        turn_id = players.index(client_address)
                        print("turn_id =", turn_id)
                        if (message[5:7] == 'up') and (message[7] == '>'):
                            print('up')
                            message = 'TURNED<{},{}>'.format(turn_id, message[5:7])
                            data = str.encode(message)
                            connection.sendall(data)
                        if (message[5:9] == 'down') and (message[9] == '>'):
                            print('down')
                            message = 'TURNED<{},{}>'.format(turn_id, message[5:9])
                            data = str.encode(message)
                            connection.sendall(data) 
                        if (message[5:9] == 'left') and (message[9] == '>'):
                            print('left')
                            message = 'TURNED<{},{}>'.format(turn_id, message[5:9])
                            data = str.encode(message)
                            connection.sendall(data)
                        if (message[5:10] == 'right') and (message[10] == '>'):
                            print('right')
                            message = 'TURNED<{},{}>'.format(turn_id, message[5:10])
                            data = str.encode(message)
                            connection.sendall(data)

                else:
                    print('no data from', client_address)
                    removePlayer(client_address)
                    print("lost connection")
                    clients.remove((connection, client_address))
                    connection.close()
                    exit()

            except:
                print('error!')
                removePlayer(client_address)
                print(player_number)
                #print(message, client_address)
                print("lost connection")
                clients.remove((connection, client_address))
                connection.close()
                exit()

    