import socket
import os #este lo a utilizar para obtener el tamaño del archivo
import hashlib #este se va a utilizar para obtener el hash del archivo
from pathlib import Path #este se va a utilizar para obtener la ruta del archivo
import struct #y este se va a utilizar para empaquetar y desempaquetar los datos


HOST = "localhost"
PORT = 9000

CARPETA_SERVIDOR = Path("archivos_servidor") #aqui se crea la carpeta donde se van a guardar los archivos que se reciban del cliente
CARPETA_SERVIDOR.mkdir(exist_ok=True)

SERVIDOR = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #aqui se crea el socket del servidor
SERVIDOR.bind((HOST, PORT))

SERVIDOR.listen()#lo ponemos en modo lectura
print("Servidor a la espera de conexiones...")

cliente, direccion = SERVIDOR.accept()
print(f"El cliente se conectó desde la dirección {direccion}")

datos = cliente.recv(1024) #este es el mensaje que se recibe del cliente
comando = datos.decode()
print(f"Comando recibido: {comando}")

#aqui se va a hacer la logica para el comando LIST
if comando == "LIST": #este es el comando que se va a utilizar para listar los archivos que se encuentran en la carpeta del servidor

    archivos = os.listdir(CARPETA_SERVIDOR)

    if len(archivos) == 0: #
        respuesta = "No hay archivos disponibles"
    else:
        respuesta = "\n".join(archivos)

    cliente.sendall(respuesta.encode())

# aqui se va a hacer la logica para el comando UPLOAD
elif comando.startswith("UPLOAD"): #este sirve para subir un archivo al servidor.

    nombre = comando.split(" ", 1)[1]

    ruta = CARPETA_SERVIDOR / nombre

    cliente.sendall(b"OK")

    # Recibir archivo
    with open(ruta, "wb") as archivo:

        while True:

            datos = cliente.recv(4096)

            if not datos:
                break

            archivo.write(datos)

    print(f"Archivo recibido: {nombre}")

#aqui se va a hacer la logica para el comando DOWNLOAD
elif comando.startswith("DOWNLOAD"): #este sirve para descargar un archivo del servidor.

    nombre = comando.split(" ", 1)[1]

    ruta = CARPETA_SERVIDOR / nombre

    if ruta.exists():

        cliente.sendall(b"OK")

        with open(ruta, "rb") as archivo:

            while True:

                datos = archivo.read(4096)

                if not datos:
                    break

                cliente.sendall(datos)

        print(f"Archivo enviado: {nombre}")

    else:

        cliente.sendall(b"ERROR: archivo no encontrado")


cliente.close()


SERVIDOR.close()