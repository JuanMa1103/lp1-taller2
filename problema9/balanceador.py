import socket
import threading

HOST = "localhost"
PORT = 9000

servidores = [ #aqui se define la lista de servidores backend a los que el balanceador enviara los clientes
    ("localhost", 9001),
    ("localhost", 9002)
]

turno = 0
lock = threading.Lock()


def servidor_activo(host, port): #este es para verificar si el servidor backend esta activo antes de enviarle un cliente
    try:
        conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conexion.settimeout(1)
        conexion.connect((host, port))
        conexion.close()
        return True
    except:
        return False


def manejar_cliente(cliente): #este es el metodo que maneja la conexion con el cliente y lo envia al servidor backend correspondiente
    global turno

    servidor = None

    with lock:
        for i in range(len(servidores)):
            posicion = (turno + i) % len(servidores)

            host, port = servidores[posicion]

            if servidor_activo(host, port):
                servidor = servidores[posicion]
                turno = posicion + 1
                break

    if servidor is None:
        cliente.sendall(b"No hay servidores disponibles\n")
        cliente.close()
        return

    try:
        host, port = servidor

        conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conexion.connect((host, port))

        print(f"Cliente enviado al servidor {port}")

        datos = cliente.recv(1024)

        if datos:
            conexion.sendall(datos)

            respuesta = conexion.recv(1024)

            if respuesta:
                cliente.sendall(respuesta)

        conexion.close()

    except Exception as e:
        print("Error:", e)

    finally:
        cliente.close()


balanceador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

balanceador.bind((HOST, PORT))
balanceador.listen()

print("Balanceador iniciado...")
print("Esperando clientes...")

while True:
    cliente, direccion = balanceador.accept()

    hilo = threading.Thread(
        target=manejar_cliente,
        args=(cliente,)
    )

    hilo.start()