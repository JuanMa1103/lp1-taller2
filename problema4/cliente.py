#!/usr/bin/env python3
"""
Problema 4: Servidor HTTP básico - Cliente
Objetivo: Crear un cliente HTTP que realice una petición GET a un servidor web local
"""

import http.client
import socket

# TODO: Definir la dirección y puerto del servidor HTTP
HOST = "localhost"
PORT = 9000
# TODO: Crear una conexión HTTP con el servidor
# HTTPConnection permite establecer conexiones HTTP con servidores
client = http.client.HTTPConnection(HOST, PORT)
client.request("GET", "/")
# TODO: Realizar una petición GET al path raíz ('/')
# request() envía la petición HTTP al servidor
# Primer parámetro: método HTTP (GET, POST, etc.)
# Segundo parámetro: path del recurso solicitado

# TODO: Obtener la respuesta del servidor
response = client.getresponse()
# getresponse() devuelve un objeto HTTPResponse con los datos de la respuesta

# TODO: Leer el contenido de la respuesta
# read() devuelve el cuerpo de la respuesta en bytes
data = response.read().decode()

# TODO: Decodificar los datos de bytes a string e imprimirlos
# decode() convierte los bytes a string usando UTF-8 por defecto
print(data)
# TODO: Cerrar la conexión con el servidor
client.close()
