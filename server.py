from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import json
import time

# Definir las variables
BUFSIZ = 1024
clients = {}
addresses = {}
clientsAddr = {}
usuarios = {}
puertos = {}

def aceptarConexionesTCP():
    while True:
        client, client_address = TCPSERVER.accept()
        print("Un nuevo cliente se ha conectado con", client_address)
        salida = 'Inicia sesion o registrate para chatear'
        listaSalida = [salida]
        client.send(bytes(json.dumps(listaSalida), "utf8"))
        addresses[client] = client_address
        Thread(target=manejarClienteTCP, args=(client,)).start()

def manejarClienteTCP(client):
    try:
        listaEntrada = json.loads(client.recv(BUFSIZ).decode("utf8"))
        name = listaEntrada[1]
        print(name)

        if listaEntrada[0] == 'Login':
            while not iniciarSesion(listaEntrada[1], listaEntrada[2]):
                salida = 'ERROR: No existe usuario o contraseña incorrecta, intente de nuevo'
                listaSalida = [salida]
                client.send(bytes(json.dumps(listaSalida), "utf8"))
                listaEntrada = json.loads(client.recv(BUFSIZ).decode("utf8"))
        elif listaEntrada[0] == 'Register':
            while registrar(listaEntrada[1]):
                salida = 'ERROR: Ya existe usuario, intente de nuevo'
                listaSalida = [salida]
                client.send(bytes(json.dumps(listaSalida), "utf8"))
                listaEntrada = json.loads(client.recv(BUFSIZ).decode("utf8"))

        usuarios[listaEntrada[1]] = listaEntrada[2]
        puertos[listaEntrada[1]] = listaEntrada[3]
        guardarDatos()
        
        welcome = 'Selecciona a quien enviar y que método. Bienvenido'
        listaSalida = [welcome]
        client.send(bytes(json.dumps(listaSalida), "utf8"))

        msg = 'Un nuevo usuario se ha conectado, checar abajo'
        listaSalida = [msg]
        clientsAddr[name] = addresses[client]
        broadcast(listaSalida)
        clients[client] = name

        while True:
            msg = client.recv(BUFSIZ)
            if not msg:
                break
            listaEntrada = json.loads(msg)

            if listaEntrada[0] == 'Enviar a':
                enviarTCP(listaEntrada, listaEntrada[1])

            if listaEntrada[0] == '*Salir*':
                listaSalida = 'Un usuario ha dejado el chat, checar abajo'
                del clients[client]
                del clientsAddr[name]
                broadcast(listaSalida)
                break

    except Exception as e:
        print(f"Error en manejarClienteTCP: {e}")
    finally:
        client.close()

def enviarTCP(lista, name):
    for sock, username in clients.items():
        if name == username:
            sock.send(bytes(json.dumps(lista), "utf8"))

def broadcast(listaSalida):
    for sock in clients:
        sock.send(bytes(json.dumps(listaSalida), "utf8"))

def conectados():
    try:
        i = 0
        while True:
            time.sleep(1)
            i += 1
            for sock in clients:
                sock.send(bytes(json.dumps(clientsAddr), "utf8"))
    except Exception as e:
        print(f"Error en conectados: {e}")

def registrar(usuario):
    return usuario in usuarios

def iniciarSesion(usuario, contraseña):
    return usuario in usuarios and usuarios[usuario] == contraseña

def manejarClientesUDP():
    while True:
        try:
            data, addr = UDPSERVER.recvfrom(BUFSIZ)
            listaEntrada = json.loads(data)
            enviarUDP(listaEntrada, listaEntrada[1])
        except Exception as e:
            print(f"Error en manejarClientesUDP: {e}")

def enviarUDP(listaSalida, name):
    UDPSERVER.sendto(bytes(json.dumps(listaSalida), "utf-8"), (clientsAddr[name][0], puertos[name]))

def cargarDatos():
    try:
        with open('numbers.txt', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardarDatos():
    try:
        with open('numbers.txt', 'w') as f:
            json.dup(usuarios, f)
    except Exception as e:
        print(f"Error en guardarDatos: {e}")

# Definir la dirección IP del servidor y puertos
HOST = '192.168.98.137'
TCPPORT = 8085
UDPPORTSERVER = 8086

ADDR_TCP = (HOST, TCPPORT)
TCPSERVER = socket(AF_INET, SOCK_STREAM)
TCPSERVER.bind(ADDR_TCP)

ADDR_UDP = (HOST, UDPPORTSERVER)
UDPSERVER = socket(AF_INET, SOCK_DGRAM)
UDPSERVER.bind(ADDR_UDP)

if __name__ == "__main__":
    TCPSERVER.listen(5)
    print("Esperando conexiones")

    aceptarTCPHilo = Thread(target=aceptarConexionesTCP)
    conectadosHilo = Thread(target=conectados)
    manejarUDPHilo = Thread(target=manejarClientesUDP)

    aceptarTCPHilo.start()
    conectadosHilo.start()
    manejarUDPHilo.start()

    try:
        aceptarTCPHilo.join()
    except KeyboardInterrupt:
        print("Servidor cerrado manualmente")

    TCPSERVER.close()
    UDPSERVER.close()
