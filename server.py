import socket
import sys
import time
from _thread import *
import time

client_messages = ('CONNECT', 'DISCONNECT', 'READY', 'TERMINATE', 'TURN')
server_messages = ('WELCOME', 'START', 'CONNECTED', 'DISCONNECTED', 'ISREADY', 'FULL', 'SPAWN', 'TERMINATED', 'VICTORY', 'TURNED')


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 10002)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(4)
sock.setblocking(False)
print('waiting for a connection')

players = ['empty', 'empty', 'empty', 'empty']
clients = []
ready_players = []
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
    #print('while')
    try:
        connection, client_address = sock.accept()
        connection.setblocking(False)
        clients.append((connection, client_address))
        print('new client: ', client_address)
        print(clients)
    
    except BlockingIOError:
        for connection, client_address in clients:
            #print('serving ', client_address)
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

                        for conn, client_a in clients:
                            message = 'WELCOME<{}>'.format(player_id)
                            data = str.encode(message)
                            conn.sendall(data)

                    if message == 'DISCONNECT':
                        removePlayer(client_address)
                        print(player_number)
                        print(message, client_address)
                        clients.remove((connection, client_address))
                        print("lost connection")
                        connection.close()
                        exit()

                    if message[0:10] == 'TERMINATE<' and (message[10] >= '0') and (message[10] <= '3') and (message[11]) == ">":
                        terminated_id = message[10]
                        ready_players.remove(int(message[10]))
                        for conn, client_a in clients:
                            message = 'TERMINATED<{}>'.format(terminated_id)
                            data = str.encode(message)
                            conn.sendall(data)

                    if message == 'READY':
                        print('received READY')
                        player_id = players.index(client_address)

                        #message = 'ISREADY<{}>'.format(player_id)
                        ready_players.append(player_id)
                        #for conn, client_a in clients:
                            #data = str.encode(message)
                            #conn.sendall(data)

                        if player_id == 0:
                            direction = 'up'
                            x_pos = 10
                            y_pos = 10
                        elif player_id == 1:
                            x_pos = 12
                            y_pos = 12
                            direction = 'down'
                        elif player_id == 2:
                            x_pos = 8
                            y_pos = 8
                            direction = 'right'
                        elif player_id == 3:
                            direction = 'left'
                            x_pos = 6
                            y_pos = 6
                        message = 'SPAWN<{},{},{},{}>'.format(player_id, direction, x_pos, y_pos)
                        for conn, client_a in clients:
                            data = str.encode(message)
                            conn.sendall(data)

                        print(len(ready_players), player_number)
                        if(len(ready_players) == player_number):
                            print('sending start!')
                            time.sleep(1)
                            for conn, client_a in clients:
                                message = 'START'
                                data = str.encode(message)
                                conn.sendall(data)

                    if message[0:5] == 'TURN<':
                        # get id
                        turn_id = players.index(client_address)
                        print("turn_id =", turn_id)
                        if (message[5:7] == 'up') and (message[7] == '>'):
                            print('up')
                            message = 'TURNED<{},{}>'.format(turn_id, message[5:7])
                            for conn, client_a in clients:
                                data = str.encode(message)
                                conn.sendall(data)
                        if (message[5:9] == 'down') and (message[9] == '>'):
                            print('down')
                            message = 'TURNED<{},{}>'.format(turn_id, message[5:9])
                            for conn, client_a in clients:
                                data = str.encode(message)
                                conn.sendall(data) 
                        if (message[5:9] == 'left') and (message[9] == '>'):
                            print('left')
                            message = 'TURNED<{},{}>'.format(turn_id, message[5:9])
                            for conn, client_a in clients:
                                data = str.encode(message)
                                conn.sendall(data)
                        if (message[5:10] == 'right') and (message[10] == '>'):
                            print('right')
                            message = 'TURNED<{},{}>'.format(turn_id, message[5:10])
                            for conn, client_a in clients:
                                data = str.encode(message)
                                conn.sendall(data)

                else:
                    print('no data from', client_address)
                    removePlayer(client_address)
                    print("lost connection")
                    clients.remove((connection, client_address))
                    connection.close()
                    exit()

            except BlockingIOError:
                pass

            except KeyboardInterrupt:
                for conn, client_a in clients:
                    conn.close()

                exit()
                #print('error!')
                #removePlayer(client_address)
                #print(player_number)
                #print(message, client_address)
                #print("lost connection")
                #clients.remove((connection, client_address))
                #connection.close()
                #exit()