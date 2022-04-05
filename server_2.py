import socket
import select
import sys
from _thread import *
# set up connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# check args passed
if len(sys.argv) != 3:
    print("Please include IP address followed by port number")
    exit()

IP_ADDR = str(sys.argv[1])
PORT = int(sys.argv[2])

server.bind((IP_ADDR, PORT))

# listens for 100 active connections
server.listen(100)

clients = []

def client_thread(connection, addr):
    connection.send("Welcome to the chatroom".encode('utf-8'))

    while True:
        try:
            msg = connection.recv(2048) # byte size
            msg = msg.decode('utf-8')
            if msg:
                full_message = "<" + addr[0] + ">" + msg
                # print source + msg
                print(full_message)

                # calls broadcast function to send msg to all
                broadcast(full_message, connection)
            
            else:
                remove(connection)
        
        except:
            continue


def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try: 
                client.send(message.encode('utf-8'))
            except: 
                client.close()
                remove(client)


def remove(connection):
    if connection in clients:
        clients.remove(connection)


while True:
    try:
        connection, addr = server.accept()
        clients.append(connection)

        # announce user that just connected
        print(addr[0] + " connected")

        # create thread for each user
        start_new_thread(client_thread, (connection, addr))
    except KeyboardInterrupt as e:
        break

connection.close()
server.close()