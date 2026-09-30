import socket
import threading

HOST = "localhost"
PORT = 9000


def manejar_cliente(cliente): #este es el hilo que maneja la conexión con el cliente
    try:
        datos = cliente.recv(1024)

        if not datos:
            cliente.close()
            return

        print("\nPetición recibida:")
        print(datos.decode(errors="ignore"))

        primera_linea = datos.decode(errors="ignore").split("\r\n")[0]# este es para recibir la peticion del cliente

        if primera_linea.startswith("CONNECT"):#este es para crear la coneccion con el servidor
            destino = primera_linea.split(" ")[1]

            host, port = destino.split(":")
            port = int(port)

            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.connect((host, port))

            cliente.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

            
            reenviar(cliente, servidor)

            servidor.close()

        else: #aqui es para reenviar la peticion al servidor y recibir la respuesta
            
            partes = primera_linea.split(" ") #este es para obtener la url de la peticion

            if len(partes) < 2:
                cliente.close()
                return

            url = partes[1]

            if url.startswith("http://"): #este es para quitar el http:// de la url
                url = url[7:]

            host = url.split("/")[0]
            ruta = "/" + "/".join(url.split("/")[1:])# y este es para obtener la ruta de la url

            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.connect((host, 80))
            
            datos = datos.replace( #este es para reemplazar la url completa por la ruta en la peticion
                b"Connection: close",
                b"Connection: keep-alive"
            )
            
            servidor.sendall(datos) 

            respuesta = servidor.recv(1024)

            while respuesta:
                cliente.sendall(respuesta)
                respuesta = servidor.recv(1024)

            servidor.close()

    except Exception as e: #este es para los errores que puedan ocurrir durante la conexión con el cliente o el servidor
        print("Error:", e)

    finally:
        cliente.close()


def reenviar(cliente, servidor): #este es para reenviar los datos entre el cliente y el servidor
    while True:
        datos = cliente.recv(1024)

        if not datos:
            break

        servidor.sendall(datos)

        respuesta = servidor.recv(1024)

        if not respuesta:
            break

        cliente.sendall(respuesta)



proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

proxy.bind((HOST, PORT))
proxy.listen()

print("Proxy iniciado...")
print("Esperando conexiones en el puerto", PORT)


while True:
    cliente, direccion = proxy.accept()

    print("Cliente conectado:", direccion)

    hilo = threading.Thread(
        target=manejar_cliente,
        args=(cliente,)
    )

    hilo.start()