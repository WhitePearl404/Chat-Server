import socket
import threading

HOST = '127.0.0.1'
PORT = 9001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknms = []

#broadcast
def broadcast(massage):
    for client in clients:
        client.send(massage)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknms[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nicknm = nicknms[index]
                broadcast(f'{nicknm} left the Chat!'.encode('utf-8'))
                nicknms.remove(nicknm)
                break

#receive
def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}!")

        client.send("admin".encode('utf-8'))
        nicknm = client.recv(1024).decode('utf-8')

        nicknms.append(nicknm)
        clients.append(client)

        print(f"Username of the client is : {nicknm}")
        broadcast(f"{nicknm} Join chat\n".encode('utf-8'))
        client.send(f"{nicknm} Connected to the server!".encode('utf-8'))


        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#handle
print("server running----")
receive()






