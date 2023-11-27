import socket
import threading
import sys

def send_messages(client_socket, target_ip, target_port):
    while True:
        message = input("")
        client_socket.sendto(message.encode(), (target_ip, target_port))
        if message.lower() == "exit":
            sys.exit()

def receive_messages(client_socket):
    while True:
        data, addr = client_socket.recvfrom(1024)
        print(f"Message from {addr}: {data.decode()}")

# Configuración del cliente
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

target_ip = input("Enter the target IP: ")
target_port = int(input("Enter the target port: "))

# Iniciar hilos para enviar y recibir mensajes
send_thread = threading.Thread(target=send_messages, args=(client, target_ip, target_port))
receive_thread = threading.Thread(target=receive_messages, args=(client,))

send_thread.start()
receive_thread.start()

