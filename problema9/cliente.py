import socket

HOST = "localhost"
PORT = 9000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((HOST, PORT))

mensaje = input("Escribe un mensaje: ")

cliente.sendall(mensaje.encode())

respuesta = cliente.recv(1024)

print("Respuesta:", respuesta.decode())

cliente.close()