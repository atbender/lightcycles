import socket
import sys
import time
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

width = 500
rows = 20
win = pygame.display.set_mode((width, width))
clock = pygame.time.Clock()





def redrawWindow(surface):
    global rows, width, s, t, snack
    surface.fill((0,0,0))
    #s.draw(surface)
    #t.draw(surface)
    # snack.draw(surface)
    # drawGrid(width,rows, surface)
    pygame.display.update()

def key_detection():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        keys = pygame.key.get_pressed()
        
        
        for key in keys:
            if keys[pygame.K_LEFT]:
                return 'left'
                #self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_RIGHT]:
                return 'right'
                #self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_UP]:
                return 'up'
                #self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_DOWN]:
                return 'down'

            elif keys[pygame.K_ESCAPE]:
                return 'esc'

    return False





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

        key = key_detection()
        print(key)
        if key == 'esc':
            message = 'DISCONNECT'
            data = str.encode(message)
            sock.sendall(data)
            break
        elif key != False:
            message = 'TURNED<' + my_id + ',' + key + '>'
            data = str.encode(message)
            sock.sendall(data)
            print(message)
        pygame.time.delay(15)
        clock.tick(15)
        #redrawWindow(win)


        data = sock.recv(2048)
        message = data.decode(encoding)
        print('received {!r}'.format(message))
        if data:
            #chunks = chunks + message
            #print(chunks)

            if (message[0:8] == "WELCOME<") and ((int(message[8:9])) >= 0) and ((int(message[8:9])) <= 3) and (message[9:10]) == ">":
                my_id = int(message[8:9])




                
                #time.sleep(5)


                
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



