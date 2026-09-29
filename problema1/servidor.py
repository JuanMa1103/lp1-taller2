#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Servidor
Objetivo: Crear un servidor TCP que acepte una conexión y intercambie mensajes básicos
"""

import socket

# TODO: Definir la dirección y puerto del servidor

HOST = "localhost"
# TODO: Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)


# TODO: Enlazar el socket a la dirección y puerto especificados
PORT = 9000
SERVIDOR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVIDOR.bind((HOST, PORT))

# TODO: Poner el socket en modo escucha
SERVIDOR.listen()

# El parámetro define el número máximo de conexiones en cola
print("Servidor a la espera de conexiones ...")

# TODO: Aceptar una conexión entrante
cliente, direccion = SERVIDOR.accept()
# accept() bloquea hasta que llega una conexión
# conn: nuevo socket para comunicarse con el cliente
# direccion: dirección y puerto del cliente

print(f"el cliente {cliente} se conecto desde la direccion {direccion}" )

# TODO: Recibir datos del cliente (hasta 1024 bytes)
datos = cliente.recv(1024)
# TODO: Enviar respuesta al cliente (convertida a bytes)

# sendall() asegura que todos los datos sean enviados
cliente.sendall(b"hola" + datos)

# TODO: Cerrar la conexión con el cliente

cliente.close()
