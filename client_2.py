# Python program to implement client side of chat room
import socket 
import select 
import sys
from _thread import *
import time

if len(sys.argv) != 3:
  print ("Correct usage: script, IP address, Username")
  exit()
IP_address = str(sys.argv[1])
Username = str(sys.argv[2])

# Server
server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_s.bind((IP_address, 8082))
server_s.listen(100)
# time.sleep(5)

# Client
connected_bool = False
while not connected_bool:
  try:
    server_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_c.connect((IP_address, 8081))
    connected_bool = True
  except:
    pass


def clientthread(conn_s, addr):
  conn_s.send("Welcome to the chatroom".encode('utf-8'))

  while True:
    # CLIENT SIDE
    sockets_list = [sys.stdin, server_c]

    read_sockets,write_socket,error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
      if socks == server_c:
        message = socks.recv(2048)
        print(message.decode('utf-8'))
      else:
        message_1 = sys.stdin.readline()
        message_2 = "<" + Username + " (YOU)" + "> " + message_1
        message_3 = "<" + Username + "> " + message_1
        message_3 = message_3.encode('utf-8')
        conn_s.send(message_3)
        sys.stdout.write(message_2)
        sys.stdout.flush()

while True:
  conn, addr = server_s.accept()

  print (addr[0] + " connected")

  start_new_thread(clientthread,(conn,addr))

server_s.close()
