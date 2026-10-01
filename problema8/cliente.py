import socket
import threading

HOST = "localhost"
PORT = 9000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))


def recibir():
    while True:
        try:
            datos = cliente.recv(1024)

            if not datos:
                break

            print(datos.decode())

        except:
            break


hilo = threading.Thread(target=recibir) 
hilo.daemon = True
hilo.start()


print("Tic-Tac-Toe")
print("Escribe un numero del 1 al 9 para jugar")

while True:
    movimiento = input("> ")

    if movimiento.lower() == "salir":
        break

    cliente.sendall(movimiento.encode())


cliente.close()