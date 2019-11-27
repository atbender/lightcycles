import socket
import sys
import time
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,color,dirnx=1,dirny=0):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
 
       
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
       
 
 
class snake(object):
    
    def __init__(self, player, color, pos):
        self.player = player
        self.color = color
        self.head = cube(pos, self.color)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 1
        self.dirny = 0
 
    def move(self):

        c = self.head

        if self.dirnx == -1 and c.pos[0] <= 0: 
            c.pos = (c.rows-1, c.pos[1])
        elif self.dirnx == 1 and c.pos[0] >= c.rows-1: 
            c.pos = (0,c.pos[1])
        elif self.dirny == 1 and c.pos[1] >= c.rows-1: 
            c.pos = (c.pos[0], 0)
        elif self.dirny == -1 and c.pos[1] <= 0: 
            c.pos = (c.pos[0],c.rows-1)
        else: 
            c.move(self.dirnx,self.dirny)



        #self.head.move(self.dirnx, self.dirny)
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
 
            keys = pygame.key.get_pressed()
 
            for key in keys:
                if keys[pygame.K_LEFT]:
                    if self.dirnx == 1:
                        return
                    self.dirnx = -1
                    self.dirny = 0
                    return
                    #self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_RIGHT]:
                    if self.dirnx == -1:
                        return
                    self.dirnx = 1
                    self.dirny = 0
                    return
                    #self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_UP]:
                    if self.dirny == 1:
                        return
                    self.dirnx = 0
                    self.dirny = -1
                    return
                    #self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_DOWN]:
                    if self.dirny == -1:
                        return
                    self.dirnx = 0
                    self.dirny = 1
                    return
                    #self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            

            '''
       
 
    def reset(self, pos):
        self.head = cube(pos, self.color)
        self.body = []
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
 
 
    def addCube(self):

        tail = self.head
        dx, dy = tail.dirnx, tail.dirny
 
        if dx == 1 and dy == 0:
            if tail.pos[0] == 0:
                self.body.append(cube((tail.rows-1, tail.pos[1]), self.color))
            else:
                self.body.append(cube((tail.pos[0]-1,tail.pos[1]), self.color))
        elif dx == -1 and dy == 0:
            if tail.pos[0] == tail.rows-1:
                self.body.append(cube((0, tail.pos[1]), self.color))
            else:
                self.body.append(cube((tail.pos[0]+1,tail.pos[1]), self.color))
        elif dx == 0 and dy == 1:
            if tail.pos[1] == 0:
                self.body.append(cube((tail.pos[0], tail.rows-1), self.color))
            else:
                self.body.append(cube((tail.pos[0],tail.pos[1]-1), self.color))
        elif dx == 0 and dy == -1:
            if tail.pos[1] == tail.rows-1:
                self.body.append(cube((tail.pos[0], 0), self.color))
            else:
                self.body.append(cube((tail.pos[0],tail.pos[1]+1), self.color))

        
 
    def draw(self, surface):
        #self.head.draw(surface, True)
        #self.body[-1].draw(surface, False)
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
 
 
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
 
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
 
        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
       
 
def redrawWindow(surface):
    global rows, width, s, t, snack
    surface.fill((0,0,0))
    s.draw(surface)
    #t.draw(surface)
    # snack.draw(surface)
    # drawGrid(width,rows, surface)
    pygame.display.update()
 
 
 
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
 



def redrawWindow(surface):
    global rows, width, s, t, snack
    surface.fill((0,0,0))
    s.draw(surface)
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
sock.setblocking(False)





global width, rows, s, t, snack
width = 500
rows = 20
win = pygame.display.set_mode((width, width))
clock = pygame.time.Clock()

s = snake(1, (255,0,0), (10,10))
#t = snake(2, (0,0,255), (14,14))
# snack = cube(randomSnack(rows, s), color=(0,255,0))
flag = True


try:
    
    # Send data
    #message = b'This is the message.  It will be repeated.'
    #print('sending {!r}'.format(message))
    message = 'CONNECT'
    data = str.encode(message)
    sock.sendall(data)

    #chunks = ''

    while True:


        try:
            data = sock.recv(2048)
            message = data.decode(encoding)
            print('received {!r}'.format(message))
            if data:
                #chunks = chunks + message
                #print(chunks)

                if (message[0:8] == "WELCOME<") and (message[8:9] >= '0') and (message[8:9] <= '3') and (message[9:10]) == ">":
                    my_id = int(message[8:9])

                if (message[0:7] == "TURNED<") and (message[7] >= '0') and (message[7] <= '3') and (message[8] == ","):
                    turned_cycle_id = int(message[7])
                    if (message[9:11] == 'up') and (message[11] == '>'):
                        print('up')
                        if s.dirny != 1:
                            s.dirnx = 0
                            s.dirny = -1
                    if (message[9:13] == 'down') and (message[13] == '>'):
                        print('down')
                        if s.dirny != -1:
                            s.dirnx = 0
                            s.dirny = 1
                    if (message[9:13] == 'left') and (message[13] == '>'):
                        print('left')
                        if s.dirnx != 1:   
                            s.dirnx = -1
                            s.dirny = 0
                    if (message[9:14] == 'right') and (message[14] == '>'):
                        print('right')
                        if s.dirnx != -1:
                            s.dirnx = 1
                            s.dirny = 0
                    
                        
            #redrawWindow(win)


                    #time.sleep(5)


                    
                    #break
                    #print('sending data back to the client')
                    #message = 'WELCOME<{}>'.format(client_address)
                    #data = str.encode(message)
                    #connection.sendall(data)

            else:
                print('no data from', server_address)
                break

        except BlockingIOError:
            key = key_detection()
            print(key)
            if key == 'esc':
                message = 'DISCONNECT'
                data = str.encode(message)
                sock.sendall(data)
                sock.close()
                exit()
            elif key != False:
                message = 'TURN<' + key + '>'
                data = str.encode(message)
                sock.sendall(data)
                print(message)


            pygame.time.delay(15)
            clock.tick(15)


            s.move()
            s.addCube()

            for x in range(len(s.body)):
                if s.body[x] != s.head and s.body[x].pos == s.head.pos:
                    print('Score: ', len(s.body))
                    message_box('You Lost!', 'Play again...')
                    s.reset((10,10))
                    break
        
            redrawWindow(win)

            
    

finally:
    print('closing socket')
    sock.close()



