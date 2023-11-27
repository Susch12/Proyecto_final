import tkinter as tk
import threading
import socket

def send_message():
    message = message_entry.get()
    if message:
        message_history.config(state=tk.NORMAL)
        message_history.insert(tk.END, f"You: {message}\n")
        message_history.config(state=tk.DISABLED)
        client.send(message.encode('utf-8'))
        message_entry.delete(0, tk.END)

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            message_history.config(state=tk.NORMAL)
            message_history.insert(tk.END, f"Other: {message}\n")
            message_history.config(state=tk.DISABLED)
        except:
            print('Error!')
            client.close()
            break

def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))

# Configuración del cliente
alias = input('Escoge un alias: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.100.134', 8085))

# Iniciar hilos para enviar y recibir mensajes
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()

# Crear la ventana principal
parent = tk.Tk()
parent.title("Chat Application")

# Crear un Text widget para el historial de mensajes
message_history = tk.Text(parent, wrap=tk.WORD, width=40, height=10)
message_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
message_history.config(state=tk.DISABLED)

# Crear un Entry widget para ingresar mensajes
message_entry = tk.Entry(parent, width=30)
message_entry.grid(row=1, column=0, padx=10, pady=10)

# Crear un botón "Send"
send_button = tk.Button(parent, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Iniciar el bucle de eventos de Tkinter
parent.mainloop()