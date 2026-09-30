import socket
import threading

HOST = "localhost"
PORT = 9000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))


def recibir(): #este es para recibir los mensajes del servidor
    while True:
        try:
            datos = cliente.recv(1024)

            if not datos:
                break

            print(datos.decode(), end="")

        except:
            break


hilo = threading.Thread(target=recibir)
hilo.daemon = True
hilo.start()


while True:
    mensaje = input()

    if mensaje.lower() == "salir":
        break

    cliente.sendall(mensaje.encode())


cliente.close()