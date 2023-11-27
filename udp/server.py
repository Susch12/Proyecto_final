import socket
import threading
import sys

clients = []

def handle_client(client_socket, client_address):
    while True:
        data, addr = client_socket.recvfrom(1024)
        

        # Reenviar el mensaje a todos los demás clientes
        for other_client, other_address in clients:
            if other_address != client_address:
                client_socket.sendto(data, other_address)

def server_main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("192.168.100.134", 8086)) 
    print("[+] El server esta en escucha...")# Usando un puerto específico (puedes cambiarlo)

    while True:
        client_data, client_address = server.recvfrom(1024)
        print(f"Se establecio conexion con: {client_address}")
        
        # Agregar el nuevo cliente a la lista
        clients.append((server, client_address))

        # Iniciar un hilo para manejar al cliente
        client_thread = threading.Thread(target=handle_client, args=(server, client_address))
        client_thread.start()

if __name__ == "__main__":
    server_main()

