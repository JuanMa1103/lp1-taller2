import socket
import threading
import sys #este modulo se importa para poder recibir argumentos desde la linea de comandos

HOST = "localhost"
PORT = int(sys.argv[1]) #este es para que el puerto se reciba desde la linea de comandos y los servidores puedan tener puertos diferentes

datos = []
lock = threading.Lock() 


def manejar_cliente(cliente): #aqui se define la funcion que maneja la conexion con el cliente
    try:
        while True:
            mensaje = cliente.recv(1024).decode()

            if not mensaje:
                break

            print("Mensaje recibido:", mensaje)

            with lock:
                datos.append(mensaje)

            cliente.sendall( 
                f"Servidor {PORT}: mensaje recibido\n".encode()
            )

    except Exception as e:
        print("Error:", e)

    finally:
        cliente.close()


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((HOST, PORT))
servidor.listen()

print(f"Servidor backend iniciado en puerto {PORT}")

while True:
    cliente, direccion = servidor.accept()

    print("Cliente conectado:", direccion)

    hilo = threading.Thread(
        target=manejar_cliente,
        args=(cliente,)
    )

    hilo.start()