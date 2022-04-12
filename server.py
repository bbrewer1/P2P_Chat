import socket
import select
import sys
from _thread import *

if len(sys.argv) != 3:
  print ("Correct usage: script, IP address, port number")
  exit()

IP_address = str(sys.argv[1])
PORT = int(sys.argv[2])

server_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_1.bind((IP_address, 8081))

server_2.bind((IP_address, 8082))

server_1.listen(100)

server_2.listen(100)

list_of_clients_1 = []

list_of_clients_2 = []

# conn_r = Receiving From
# conn_s = Sending To
def clientthread(conn_r, conn_s, addr, list_of_clients):
  conn_s.send("Welcome to the chatroom".encode('utf-8'))

  while True:
    try:
      message = conn_r.recv(2048)
      message = message.decode('utf-8')
      if message:
        message_2 = "<" + addr[0] + "> " + message

        print(message_2)

        broadcast(message_2, conn_r)
      else:
        remove(conn_s)

    except:
      continue

def broadcast(message, connection, list_of_clients):
  for clients in list_of_clients:
    if clients!=connection:
      try:
        clients.send(message.encode('utf-8'))
      except:
        clients.close()
        remove(clients, list_of_clients)

def remove(connection, list_of_clients):
  if connection in list_of_clients:
    list_of_clients.remove(connection)

while True:
  conn_1, addr_1 = server_1.accept()
  conn_2, addr_2 = server_2.accept()
  list_of_clients_1.append(conn_1)
  list_of_clients_2.append(conn_2)

  print (addr_1[0] + " connected")
  print (addr_2[0] + " connected")

  start_new_thread(clientthread,(conn_1, conn_2, addr_1,list_of_clients_2))	
  start_new_thread(clientthread,(conn_2, conn_1, addr_2,list_of_clients_1))

conn_1.close()
conn_2.close()
server_1.close()
server_2.close()
