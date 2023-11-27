'Chat Room Connection - Client-To-Client'
import threading
import socket
host = '192.168.100.134'
port = 8085
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []


def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle clients'connections


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(alias+' dejo el chat!'.encode('utf-8'))
            aliases.remove(alias)
            break
# Main function to receive the clients connection


def receive():
    while True:
        print('[+] El servidor esta en escucha...')
        client, address = server.accept()
        print(f'[+] Se establecio conexion con: {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print('Se tomo el alias como: '+ alias.decode('utf-8'))
        broadcast(alias+' se ha conectado al chat'.encode('utf-8'))
        client.send('Ya estas conectado!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
