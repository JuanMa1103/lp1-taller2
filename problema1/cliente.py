#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Cliente
Objetivo: Crear un cliente TCP que se conecte a un servidor e intercambie mensajes básicos
"""

import socket

# TODO: Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)

HOST = "localhost"
PORT = 9000
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TODO: Conectar el socket al servidor en la dirección y puerto especificados
cliente.connect((HOST, PORT))

# TODO: Enviar datos al servidor (convertidos a bytes)
# sendall() asegura que todos los datos sean enviados
cliente.sendall(b"hola servidor")

# TODO: Recibir datos del servidor (hasta 1024 bytes)
datos = cliente.recv(1024)

# TODO: Decodificar e imprimir los datos recibidos
print(f"Respuesta: {datos.decode()}")

# TODO: Cerrar la conexión con el servidor
cliente.close()
