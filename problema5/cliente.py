import socket


HOST = "localhost"
PORT = 9000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))


#aqui estoy creando un menu para que el usuario pueda elegir que comando quiere ejecutar
print("===== TRANSFERENCIA DE ARCHIVOS =====")
print("1. LIST")
print("2. UPLOAD")
print("3. DOWNLOAD")

opcion = input("Seleccione una opción: ")

if opcion == "1": #si elege el uno se va a ejecutar el comando LIST

    cliente.sendall(b"LIST")

    datos = cliente.recv(4096)

    print("\nArchivos disponibles:")
    print(datos.decode())
    
elif opcion == "2": #si elige el dos se va a ejecutar el comando UPLOAD

    nombre = input("Nombre del archivo: ")

    cliente.sendall(f"UPLOAD {nombre}".encode())

    respuesta = cliente.recv(1024)

    if respuesta == b"OK":

        with open(nombre, "rb") as archivo:

            while True:

                datos = archivo.read(4096)

                if not datos:
                    break

                cliente.sendall(datos)

        print("Archivo enviado correctamente")

elif opcion == "3": #y si elige el tres se va a ejecutar el comando DOWNLOAD

    nombre = input("Nombre del archivo: ")

    cliente.sendall(f"DOWNLOAD {nombre}".encode())

    respuesta = cliente.recv(1024)

    if respuesta == b"OK":

        with open(nombre, "wb") as archivo:

            while True:

                datos = cliente.recv(4096)

                if not datos:
                    break

                archivo.write(datos)

        print("Archivo descargado correctamente")

    else:

        print(respuesta.decode())

cliente.close()