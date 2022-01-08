from socket import *
# connect to server
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

# start program
print("-----start game-----")
name = input("Enter name: ")
# print('Your balance is 0')
# print('Please Deposit!')

# send request
clientSocket.sendto(name.encode(), (serverName, serverPort))

while True:
    response, serverAddress = clientSocket.recvfrom(2048)
    if(response.decode() == '400'):
        print('Server is full')
        clientSocket.close()
        break
    print(response.decode())

    response, serverAddress = clientSocket.recvfrom(2048)

    if(response.decode() == '200'):
        start = input('Type start to start game: ')
        clientSocket.sendto(start.encode(), (serverName, serverPort))
    else:
        print(response.decode())

    while True:
        response, serverAddress = clientSocket.recvfrom(2048)

        if(response.decode() == '400'):
            start = input('Type start to start game: ')
            clientSocket.sendto(start.encode(), (serverName, serverPort))
            continue

        if(response.decode() == '200'):
            print('Wait opponent play ...')
        elif('YOU WIN' in response.decode() or 'YOU LOSE' in response.decode() or 'YOU DRAW' in response.decode()):
            print(name +', '+ response.decode())
            clientSocket.close()
            break
        else:
            print(response.decode())
            play  = input('Select your placed: ')
            clientSocket.sendto(play.encode(), (serverName, serverPort))
    break     