import tkinter as tk
import socket
import threading
import sys

def send_messages(client_socket, target_ip, target_port):
    while True:
        message = message_entry.get()
        if message:
            client_socket.sendto(message.encode(), (target_ip, target_port))
            if message.lower() == "exit":
                sys.exit()

def receive_messages(client_socket):
    while True:
        data, addr = client_socket.recvfrom(1024)
        message_history.config(state=tk.NORMAL)
        message_history.insert(tk.END, f"Target: {data.decode()} from {addr}\n")
        message_history.config(state=tk.DISABLED)

# Configuración del cliente
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get target IP and port from user input
target_ip = input("Enter the target IP: ")
target_port = int(input("Enter the target port: "))

# Iniciar hilos para enviar y recibir mensajes
send_thread = threading.Thread(target=send_messages, args=(client, target_ip, target_port))
receive_thread = threading.Thread(target=receive_messages, args=(client,))

send_thread.start()
receive_thread.start()

# Function to send a message
def send_message():
    message = message_entry.get()
    if message:
        message_history.config(state=tk.NORMAL)
        message_history.insert(tk.END, f"Tu: {message}\n")
        message_history.config(state=tk.DISABLED)
        client.sendto(message.encode(), (target_ip, target_port))
        message_entry.delete(0, tk.END)

# Create the main window
parent = tk.Tk()
parent.title("Chat")

# Create a Text widget for message history
message_history = tk.Text(parent, wrap=tk.WORD, width=40, height=10)
message_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
message_history.config(state=tk.DISABLED)

# Create an Entry widget for entering messages
message_entry = tk.Entry(parent, width=30, text = 'Escribe tu mensaje')
message_entry.grid(row=1, column=0, padx=10, pady=10)

# Create a "Send" button
send_button = tk.Button(parent, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Start the Tkinter event loop
parent.mainloop()
