import tkinter as tk
import subprocess

def scriptTCP_click():
    etiqueta.config(text="TCP")
    serverTCP = "/home/susch/Documentos/Sistemas_Operativos/test/tcp/server.py"
    procesoTCP = subprocess.run(["python3",serverTCP])

def scriptUDP_click():
    etiqueta.config(text="UDP")
    serverUDP = "/home/susch/Documentos/Sistemas_Operativos/test/udp/server.py"
    procesoUDP = subprocess.run(["python3",serverUDP])    #ventana principal

ventana = tk.Tk()
ventana.title("Menu")

# Crear etiqueta
etiqueta = tk.Label(ventana, text="Escoge el protocolo")

# Crear botones
boton1 = tk.Button(ventana, text="TCP", command=scriptTCP_click)
boton2 = tk.Button(ventana, text="UDP", command=scriptUDP_click)

# Colocar elementos en la ventana
etiqueta.pack(pady=10)
boton1.pack(pady=5)
boton2.pack(pady=5)

# Iniciar el bucle principal
ventana.mainloop()





