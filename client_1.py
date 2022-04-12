# Python program to implement client side of chat room
import socket 
import select 
import sys
from _thread import *
import time

if len(sys.argv) != 2:
  print ("Correct usage: script, IP address")
  exit()
IP_address = str(sys.argv[1])

# Server
server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_s.bind((IP_address, 8081))
server_s.listen(100)
time.sleep(3)

# Client
server_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_c.connect((IP_address, 8082))

def clientthread(conn_s, addr):
  conn_s.send("Welcome to the chatroom - Client 2".encode('utf-8'))

  while True:
    # CLIENT SIDE
    sockets_list = [sys.stdin, server_c]

    read_sockets,write_socket,error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
      if socks == server_c:
        message = socks.recv(2048)
        print("<" + addr[0] + "> " + message.decode('utf-8'))
      else:
        message = sys.stdin.readline()
        conn_s.send(message.encode('utf-8'))
        sys.stdout.write("<Client1>")
        sys.stdout.write(message)
        sys.stdout.flush()

while True:
  conn, addr = server_s.accept()

  print (addr[0] + " connected")

  start_new_thread(clientthread,(conn,addr))

server_s.close()
