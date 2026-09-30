import socket

HOST = "localhost"
PORT = 9000

proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

proxy.connect((HOST, PORT))

peticion = ( #esta es la peticion que se envia al proxy
    "GET http://ejemplo.com/ HTTP/1.1\r\n"
    "Host: ejemplo.com\r\n"
    "Connection: close\r\n"
    "\r\n"
)

proxy.sendall(peticion.encode())

respuesta = proxy.recv(1024)

while respuesta: #este es para recibir la respuesta del proxy y mostrarla en pantalla
    print(respuesta.decode(errors="ignore"))
    respuesta = proxy.recv(1024)

proxy.close()