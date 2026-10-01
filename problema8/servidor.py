import socket
import threading

HOST = "localhost"
PORT = 9000

jugadores = [] #esta es para los jugadores que se conectan al servidor
espectadores = [] #esta es para los espectadores que se conectan al servidor
tablero = [" "] * 9 #esta es la cantidad de posiciones que tiene el tablero de juego
turno = 0

lock = threading.Lock() #este eslos juagdores puedan acceder al tablero de juego y evitar que los hilos se choquen entre si.


def enviar(cliente, mensaje):
    cliente.sendall(mensaje.encode())


def mostrar_tablero(): #aqui se esta creando el tablero dejuego que se va a mostrar en la consola de los jugadores.
    return f"""
 {tablero[0]} | {tablero[1]} | {tablero[2]}
---+---+---
 {tablero[3]} | {tablero[4]} | {tablero[5]}
---+---+---
 {tablero[6]} | {tablero[7]} | {tablero[8]}
"""


def ganador(): #con este se mira si hay un ganador, u perdedor o si hay empate.
    combinaciones = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in combinaciones:
        if tablero[a] != " " and tablero[a] == tablero[b] == tablero[c]:
            return tablero[a]

    if " " not in tablero:
        return "EMPATE"

    return None


def manejar_cliente(cliente):
    global turno

    try:
        if len(jugadores) < 2: #este es para que los jugadores puedan conectarse al servidor y jugar el juego de Tic-Tac-Toe
            jugadores.append(cliente)

            if len(jugadores) == 1:
                simbolo = "X"
                enviar(cliente, "Eres jugador X\n")
            else:
                simbolo = "O"
                enviar(cliente, "Eres jugador O\n")

            enviar(cliente, mostrar_tablero())

            while True:
                mensaje = cliente.recv(1024).decode().strip()

                if not mensaje:
                    break

                if jugadores[turno] != cliente: #este es para que los jugadores jueguen en el turno que les corresponde.
                    enviar(cliente, "No es tu turno\n")
                    continue

                try:
                    posicion = int(mensaje) - 1
                except:
                    enviar(cliente, "Escribe una posicion del 1 al 9\n")
                    continue

                with lock: 
                    if posicion < 0 or posicion > 8:
                        enviar(cliente, "Posicion invalida\n")
                        continue

                    if tablero[posicion] != " ":
                        enviar(cliente, "Esa posicion ya esta ocupada\n")
                        continue

                    tablero[posicion] = simbolo

                    resultado = ganador()

                    mensaje_tablero = mostrar_tablero()

                    for jugador in jugadores:
                        enviar(jugador, mensaje_tablero)

                    for espectador in espectadores:
                        enviar(espectador, mensaje_tablero)

                    if resultado:
                        for jugador in jugadores:
                            enviar(jugador, f"Resultado: {resultado}\n")
                        break

                    turno = 1 - turno

        else: #este es para que los jugadores puedan conectarse al servidor y jugar el juego de Tic-Tac-Toe
            espectadores.append(cliente)

            enviar(cliente, "Eres espectador\n")
            enviar(cliente, mostrar_tablero())

            while True:
                datos = cliente.recv(1024)

                if not datos:
                    break

    except Exception as e: 
        print("Error:", e)

    finally:
        if cliente in jugadores:
            jugadores.remove(cliente)

        if cliente in espectadores:
            espectadores.remove(cliente)

        cliente.close()


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((HOST, PORT))
servidor.listen()

print("Servidor de Tic-Tac-Toe iniciado...")
print("Esperando jugadores...")

while True:
    cliente, direccion = servidor.accept()

    print("Cliente conectado:", direccion)

    hilo = threading.Thread(
        target=manejar_cliente,
        args=(cliente,)
    )

    hilo.start()