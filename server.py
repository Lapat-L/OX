from socket import *
import random
# init server
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

# person


class Person:
    def __init__(self, name, score):
        self.name = name
        self.score = score


print("The server is ready to receive in port:", serverPort)
player = 0
player1 = ''
player2 = ''
start = 0
while True:
    player+=1
    message, clientAddress = serverSocket.recvfrom(2048) 
    if(player==1):
        player1 = clientAddress
        serverSocket.sendto('You are player 1 (O)\nWaiting for player 2 ...'.encode(), player1)  
    elif(player==2):
        player2 = clientAddress
        serverSocket.sendto('You are player 2 (X)'.encode(), player2)
        serverSocket.sendto('200'.encode(), player1)
        serverSocket.sendto('Wait for player 1 to start game ...'.encode(), player2)
    else:
        if(clientAddress == player1 or clientAddress == player2):
            if(message.decode().lower() == 'start' and start == 0):
                start=1
                serverSocket.sendto('200'.encode(), player2)
                string = '1|2|3\n_ _ _\n4|5|6\n_ _ _\n7|8|9'
                serverSocket.sendto(string.encode(), player1)  
            else:
                try:
                    x = message.decode()
                    int(x)
                except:
                    continue
                if(string.count(message.decode())!=1):
                    if(clientAddress == player1):
                        out = message.decode()+' are already placed\nPlease placed again.\n'+string
                        serverSocket.sendto(out.encode(), player1)
                    else:
                        out = message.decode()+' are already placed\nPlease placed again.\n'+string
                        serverSocket.sendto(out.encode(), player2)
                    continue
                if(clientAddress == player1):
                    string = string.replace(message.decode(), 'O')
                    x = string.count('X')
                    o = string.count('O')
                    total = o+x
                    if(string.find('O|O|O') != -1):
                        # player 1 win
                        start = 0
                        player = 0
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif(string.find('X|X|X') != -1):
                        # player 2 win 
                        start = 0
                        player = 0
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif((string[0]==string[12]==string[24]=='O') or (string[2]==string[14]==string[26]=='O') or (string[4]==string[16]==string[28]=='O')):
                        # player 1 win
                        start = 0
                        player = 0
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif((string[0]==string[14]==string[28]=='O') or (string[4]==string[14]==string[24]=='O')):
                        # player 1 win
                        start = 0
                        player = 0
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif((string[0]==string[12]==string[24]=='X') or (string[2]==string[14]==string[26]=='X') or (string[4]==string[16]==string[28]=='X')):
                        # player 2 win
                        start = 0
                        player = 0
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif((string[0]==string[14]==string[28]=='X') or (string[4]==string[14]==string[24]=='X')):
                        # player 2 win
                        start = 0
                        player = 0
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif(total==9):
                        # draw
                        start = 0
                        player = 0
                        out = 'YOU DRAW\n'+string
                        serverSocket.sendto(out.encode(), player1)
                        serverSocket.sendto(out.encode(), player2)
                        continue
                    serverSocket.sendto('200'.encode(), player1)
                    serverSocket.sendto(string.encode(), player2) 
                else:
                    string = string.replace(message.decode(), 'X')
                    x = string.count('X')
                    o = string.count('O')
                    total = o+x
                    if(string.find('O|O|O') != -1):
                        # player 1 win
                        start = 0
                        player = 0
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif(string.find('X|X|X') != -1):
                        # player 2 win 
                        start = 0
                        player = 0
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif((string[0]==string[12]==string[24]=='O') or (string[2]==string[14]==string[26]=='O') or (string[4]==string[16]==string[28]=='O')):
                        # player 1 win
                        start = 0
                        player = 0
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif((string[0]==string[14]==string[28]=='O') or (string[4]==string[14]==string[24]=='O')):
                        # player 1 win
                        start = 0
                        player = 0
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif((string[0]==string[12]==string[24]=='X') or (string[2]==string[14]==string[26]=='X') or (string[4]==string[16]==string[28]=='X')):
                        # player 2 win
                        start = 0
                        player = 0
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif((string[0]==string[14]==string[28]=='X') or (string[4]==string[14]==string[24]=='X')):
                        # player 2 win
                        start = 0
                        player = 0
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        serverSocket.sendto(out2.encode(), player2)
                        continue
                    elif(total==9):
                        # draw
                        start = 0
                        player = 0
                        out = 'YOU DRAW\n'+string
                        serverSocket.sendto(out.encode(), player1)
                        serverSocket.sendto(out.encode(), player2)
                        continue
                    serverSocket.sendto('200'.encode(), player2)
                    serverSocket.sendto(string.encode(), player1) 
        else:
            serverSocket.sendto('400'.encode(), clientAddress)