import socket
import threading #este nos permite crear hilos para manejar mutiples clientes
import os # este nos permite interactuar con el sistema operativo, como crear carpetas y archivos

HOST = "localhost"
PORT = 9000

salas = {} #aqui se creo una ireccion para las salas
clientes = {} #aca se creo una direccion para los clientes
lock = threading.Lock() # y este comando es para que las direcciones no choquen entre si


def enviar(cliente, mensaje):
    cliente.sendall(mensaje.encode())


def manejar_cliente(cliente, direccion): #esta se creo para manejar los clientes
    try:
        enviar(cliente, "Escribe tu nombre: ")
        nombre = cliente.recv(1024).decode().strip()

        with lock:
            clientes[nombre] = cliente

        enviar(cliente, "Bienvenido " + nombre + "\n")
        enviar(cliente, "Comandos: CREATE, JOIN, LEAVE, LIST, MSG, PM\n")

        while True:
            datos = cliente.recv(1024)

            if not datos:
                break

            mensaje = datos.decode().strip()
            partes = mensaje.split(" ", 2)

            comando = partes[0].upper()

            if comando == "CREATE" and len(partes) >= 2: #este comando es para crear las salas y si la sala ya existe no se creara otra
                sala = partes[1]

                with lock:
                    if sala not in salas:
                        salas[sala] = set()
                        enviar(cliente, f"Sala '{sala}' creada\n")
                    else:
                        enviar(cliente, "La sala ya existe\n")

            elif comando == "JOIN" and len(partes) >= 2: #este es para unirse a una sala
                sala = partes[1]

                with lock:
                    if sala in salas:
                        salas[sala].add(nombre)
                        enviar(cliente, f"Entraste a {sala}\n")
                    else:
                        enviar(cliente, "La sala no existe\n")

            elif comando == "LEAVE" and len(partes) >= 2: #este es para salir de la sala
                sala = partes[1]

                with lock:
                    if sala in salas and nombre in salas[sala]:
                        salas[sala].remove(nombre)
                        enviar(cliente, f"Saliste de {sala}\n")
                    else:
                        enviar(cliente, "No estas en esa sala\n")

            elif comando == "LIST": #este es para ver las salas y los usuarios que estan en ellas
                with lock:
                    texto = "Salas:\n"

                    for sala, usuarios in salas.items():
                        texto += f"- {sala}: {', '.join(usuarios)}\n"

                enviar(cliente, texto)

            elif comando == "MSG" and len(partes) >= 2: #este es para enviar mensajes a todos los usuarios de la sala
                texto = partes[1] if len(partes) == 2 else partes[1] + " " + partes[2]

                with lock:
                    for sala, usuarios in salas.items():
                        if nombre in usuarios:
                            for usuario in usuarios:
                                if usuario in clientes:
                                    enviar(
                                        clientes[usuario],
                                        f"[{sala}] {nombre}: {texto}\n"
                                    )

            elif comando == "PM" and len(partes) >= 3: #este es para enviar mensajes privados a un usuario en especifico
                destinatario = partes[1]
                texto = partes[2]

                with lock:
                    if destinatario in clientes:
                        enviar(
                            clientes[destinatario],
                            f"[Privado de {nombre}] {texto}\n"
                        )
                        enviar(cliente, "Mensaje privado enviado\n")
                    else:
                        enviar(cliente, "Usuario no encontrado\n")

            else:
                enviar(cliente, "Comando no valido\n")

    except Exception as e:
        print("Error:", e)

    finally: #este es para cerrar la conexion con el cliente
        with lock:
            if nombre in clientes:
                del clientes[nombre]

            for sala in salas:
                salas[sala].discard(nombre)

        cliente.close()
        print(f"{nombre} se desconecto")


def guardar_salas(): #este es para guardar las salas en un archivo de texto
    with open("salas.txt", "w") as archivo:
        for sala in salas:
            archivo.write(sala + "\n")


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print("Servidor iniciado...")
print("Esperando conexiones...")

while True:
    cliente, direccion = servidor.accept()

    hilo = threading.Thread(
        target=manejar_cliente,
        args=(cliente, direccion)
    )

    hilo.start()