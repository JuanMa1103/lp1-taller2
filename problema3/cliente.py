import socket
import threading

HOST = "localhost"
PORT = 9000

def recibir_mensajes(client_socket):
    """
    Función para recibir mensajes del servidor y mostrarlos en la consola.
    
    Args:
        client_socket: Socket del cliente
    """
    while True:
        mensaje = client_socket.recv(1024).decode()
        print(mensaje)

nombre = input("Ingrese su nombre: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(nombre.encode())

hilo_recibir = threading.Thread(target=recibir_mensajes, args=(client_socket,))
hilo_recibir.start()

while True:
    mensaje = input("ingresa mensaje:")
    client_socket.send(mensaje.encode())