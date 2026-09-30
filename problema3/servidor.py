#!/usr/bin/env python3
"""
Problema 3: Chat simple con múltiples clientes - Servidor
Objetivo: Crear un servidor de chat que maneje múltiples clientes simultáneamente usando threads
"""

import socket
import threading

# TODO: Definir la dirección y puerto del servidor
HOST = "localhost"
PORT = 9000

# Lista para mantener todos los sockets de clientes conectados
clients = []

def atender_client(client_socket, client_name):
    """
    Maneja la comunicación con un cliente específico en un hilo separado.
    
    Args:
        client_socket: Socket del cliente
        client_name: Nombre del cliente
    """
    while True:
        try:
            # TODO: Recibir datos del cliente (hasta 1024 bytes)
            mensaje = client_socket.recv(1024)
            data = client_socket.recv(1024)

            # Si no se reciben datos, el cliente se desconectó
            if not data:
                break
            print(f"Mensaje recibido de {client_name}: {data.decode()}")

            #Formatear el mensaje con el nombre del cliente
            message = f"{client_name}: {data.decode()}"

            broadcast(message, client_socket)

            # Imprimir el mensaje en el servidor
            print(message)

        except ConnectionResetError:
            # Manejar desconexión inesperada del cliente
            if client_socket in clients:
                clients.remove(client_socket)

            client_socket.close()
            break


def broadcast(message, sender_socket):
    """
    Envía un mensaje a todos los clientes conectados excepto al remitente.
    
    Args:
        message: Mensaje a enviar (string)
        sender_socket: Socket del cliente que envió el mensaje original
    """

    # TODO: Retransmitir el mensaje a todos los clientes excepto al remitente
    for client in clients:
        if client != sender_socket:
            try:
                # TODO: Enviar el mensaje codificado a bytes a cada cliente
                client.send(message.encode())
            except:
                pass  # Manejar errores de envío (por ejemplo, cliente desconectado)


# TODO: Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TODO: Enlazar el socket a la dirección y puerto especificados
server_socket.bind((HOST, PORT))

# TODO: Poner el socket en modo escucha
# El parámetro define el número máximo de conexiones en cola
server_socket.listen(5)

print("Servidor a la espera de conexiones ...")


# Bucle principal para aceptar conexiones entrantes
while True:
    # TODO: Aceptar una conexión entrante
    # client: nuevo socket para comunicarse
    client_socket, client_address = server_socket.accept()
    print(f"Conexión establecida con {client_address}")
    name = client_socket.recv(1024).decode()
    clients.append(client_socket)
    broadcast(f"{name} se ha unido al chat.", client_socket)
    hilo = threading.Thread(target=atender_client, args=(client_socket, name))
    hilo.start()