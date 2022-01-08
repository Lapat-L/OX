from socket import *
# connect to server
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

# start program
print("-----start game-----")
name = input("Enter name: ")

# send request
clientSocket.sendto(name.encode(), (serverName, serverPort))

while True:
    # รับข้อความแสดงสถานะของผ้เล่น
    response, serverAddress = clientSocket.recvfrom(2048)

    # กรณีห้องเต็ม(มีผู้เล่นแล้ว 2 คนใน server) 400
    if(response.decode() == '400'):
        print('Server is full')
        clientSocket.close()
        break

    # แสดงข้อมูลสถานะของผู้เล่น 201
    print(response.decode())

    # รับสถานะเพื่อกำหนดการกระทำลำดับต่อไป
    response, serverAddress = clientSocket.recvfrom(2048)

    # 200 ผู้เล่นครบจำนวนรอผู้เล่น 1 เริ่มการแข่งขัน
    if(response.decode() == '200'):
        start = input('Type start to start game: ')
        clientSocket.sendto(start.encode(), (serverName, serverPort))
    # 201 รอผู้เล่นคนที่ 1 เริ่มการแข่งขัน
    else:
        print(response.decode())

    while True:

        # รับข้อความจาก server เพื่อกำหนดการกระทำต่อไป
        response, serverAddress = clientSocket.recvfrom(2048)

        # 401 เขียน start ไม่ถูกต้อง
        if(response.decode() == '400'):
            start = input('Type start to start game: ')
            clientSocket.sendto(start.encode(), (serverName, serverPort))
            continue

        # 201 ผู้เล่นรอคู่แข่งเลือกตำแหน่ง
        if(response.decode() == '200'):
            print('Wait opponent play ...')
        # 203 รู้ผลการแข่งขัน
        elif('YOU WIN' in response.decode() or 'YOU LOSE' in response.decode() or 'YOU DRAW' in response.decode()):
            print(name +', '+ response.decode())
            clientSocket.close()
            break
        # 401 ผู้เล่นใส่ตำแหน่งไม่ถูกต้อง /202 ถึง turn ผู้เล่นเลือกตำแหน่ง 
        else:
            print(response.decode())
            play  = input('Select your placed: ')
            clientSocket.sendto(play.encode(), (serverName, serverPort))
    break     