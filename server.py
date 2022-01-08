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
# player คือจำนวน request จาก client 
player = 0
# address ของผู้เล่นคนที่ 1
player1 = ''
# address ของผู้เล่นคนที่ 2
player2 = ''
# สถานะของเกม 0 คือยังไม่มีการเริ่มเกม 1 คือมีเกมกำลังดำเนินอยู่
start = 0
while True:
    player+=1
    # รับ request จากผู้เล่นเพื่อเก็บ address
    message, clientAddress = serverSocket.recvfrom(2048)

    # 201 กรณีเป็นผู้เล่นคนที่ 1
    if(player==1):
        player1 = clientAddress
        serverSocket.sendto('You are player 1 (O)\nWaiting for player 2 ...'.encode(), player1)  
        print(201)
    # 200/201 กรณีผู้เล่นคนที่ 2
    elif(player==2):
        player2 = clientAddress
        serverSocket.sendto('You are player 2 (X)'.encode(), player2)
        print(201)
        serverSocket.sendto('200'.encode(), player1)
        print(200)
        serverSocket.sendto('Wait for player 1 to start game ...'.encode(), player2)
        print(200)
    # กรณีผู้เล่นตั้งแต่คนที่ 3 เป็นต้นไป และกรณีรับคำสั่งในระหว่างเล่นเกม
    else:
        # กรณีผู้ส่ง request เป็นผู้เล่นคนที่ 1 และ 2
        if(clientAddress == player1 or clientAddress == player2):
            # รับคำสั่ง start จากผู้เล่นคนที่ 1 
            if(message.decode().lower() == 'start' and start == 0):
                start=1
                # 201 ส่งสถานะเพื่อแจ้งว่าเกมเริ่มแล้วให้รอผู้เล่นคนที่หนึ่งเลือกวางตำแหน่ง
                serverSocket.sendto('200'.encode(), player2)
                print(200)
                string = '1|2|3\n_ _ _\n4|5|6\n_ _ _\n7|8|9'
                # 202 ส่งข้อมูลเพื่อให้ผู้เล่นคนที่ 1 เลือกตำแหน่งการวาง
                serverSocket.sendto(string.encode(), player1)
                print(202) 
            # 401 กรณีผู้เล่นคนที่เขียน start ผิด  
            elif(message.decode().lower() != 'start' and start == 0):
                serverSocket.sendto('400'.encode(), player1)
                print(401)
            else:
                # ตรวจสอบว่า ตำแหน่งที่รับมาเป็นตัวเลขหรือไม่
                try:
                    x = message.decode()
                    int(x)
                except:
                    # 401 กรณีรับข้อมูลที่ไม่ใช่ตัวเลข
                    if(clientAddress == player1):
                        out = message.decode()+' is not a number\nPlease place again.\n'+string
                        serverSocket.sendto(out.encode(), player1)
                    else:
                        out = message.decode()+' is not a number\nPlease place again.\n'+string
                        serverSocket.sendto(out.encode(), player2)
                    print(401)
                    continue
                # ตรวจสอบว่าตำแหน่งนั้นมีการวางไปหรือยัง
                if(string.count(message.decode())!=1):
                    # 401 กรณีที่เลขตำแหน่งไม่ถูกต้อง
                    if(int(message.decode()) < 0 or int(message.decode()) > 9):
                        if(clientAddress == player1):
                            out = message.decode()+' isn\'t number of placed\nPlease place again.\n'+string
                            serverSocket.sendto(out.encode(), player1)
                        else:
                            out = message.decode()+' isn\'t number of placed\nPlease place again.\n'+string
                            serverSocket.sendto(out.encode(), player2)
                        print(401)
                        continue
                    # 401 กรณีตำแหน่งนั้นได้ถูกวางแล้ว
                    if(clientAddress == player1):
                        out = message.decode()+' is already place\nPlease place again.\n'+string
                        serverSocket.sendto(out.encode(), player1)
                    else:
                        out = message.decode()+' is already place\nPlease place again.\n'+string
                        serverSocket.sendto(out.encode(), player2)
                    print(401)
                    continue
                # ตรวจสอบว่า request มาจากผู้เล่นคนใดเพื่อส่ง response
                if(clientAddress == player1):
                    string = string.replace(message.decode(), 'O')
                    x = string.count('X')
                    o = string.count('O')
                    total = o+x
                    # ตรวจสอบผลการแข่งขัน
                    if(string.find('O|O|O') != -1):
                        # player 1 win
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif(string.find('X|X|X') != -1):
                        # player 2 win 
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif((string[0]==string[12]==string[24]=='O') or (string[2]==string[14]==string[26]=='O') or (string[4]==string[16]==string[28]=='O')):
                        # player 1 win
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif((string[0]==string[14]==string[28]=='O') or (string[4]==string[14]==string[24]=='O')):
                        # player 1 win
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif((string[0]==string[12]==string[24]=='X') or (string[2]==string[14]==string[26]=='X') or (string[4]==string[16]==string[28]=='X')):
                        # player 2 win
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif((string[0]==string[14]==string[28]=='X') or (string[4]==string[14]==string[24]=='X')):
                        # player 2 win
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif(total==9):
                        # draw
                        out = 'YOU DRAW\n'+string
                        serverSocket.sendto(out.encode(), player1)
                        print(203)
                        serverSocket.sendto(out.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    # หากหลังจากวางตำแหน่งแล้วยังไม่จบการแข่งขันส่ง response ให้ client เพื่อดำเนินเกมต่อ
                    serverSocket.sendto('200'.encode(), player1)
                    print(201)
                    serverSocket.sendto(string.encode(), player2)
                    print(202) 
                else:
                    string = string.replace(message.decode(), 'X')
                    x = string.count('X')
                    o = string.count('O')
                    total = o+x
                    if(string.find('O|O|O') != -1):
                        # player 1 win
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif(string.find('X|X|X') != -1):
                        # player 2 win 
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif((string[0]==string[12]==string[24]=='O') or (string[2]==string[14]==string[26]=='O') or (string[4]==string[16]==string[28]=='O')):
                        # player 1 win
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif((string[0]==string[14]==string[28]=='O') or (string[4]==string[14]==string[24]=='O')):
                        # player 1 win
                        out1 = 'YOU WIN\n'+string
                        out2 = 'YOU LOSE\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif((string[0]==string[12]==string[24]=='X') or (string[2]==string[14]==string[26]=='X') or (string[4]==string[16]==string[28]=='X')):
                        # player 2 win
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif((string[0]==string[14]==string[28]=='X') or (string[4]==string[14]==string[24]=='X')):
                        # player 2 win
                        out1 = 'YOU LOSE\n'+string
                        out2 = 'YOU WIN\n'+string
                        serverSocket.sendto(out1.encode(), player1)
                        print(203)
                        serverSocket.sendto(out2.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    elif(total==9):
                        # draw
                        out = 'YOU DRAW\n'+string
                        serverSocket.sendto(out.encode(), player1)
                        print(203)
                        serverSocket.sendto(out.encode(), player2)
                        print(203)
                        start = 0
                        player = 0
                        player1 = ''
                        player2 = ''
                        continue
                    serverSocket.sendto('200'.encode(), player2)
                    print(201)
                    serverSocket.sendto(string.encode(), player1)
                    print(202) 
        # 400 กรณีผู้ส่ง request ตั้งแต่อันที่ 3 ที่ไม่ใช่ผู้เล่นเกม
        else:
            serverSocket.sendto('400'.encode(), clientAddress)
            print(400)