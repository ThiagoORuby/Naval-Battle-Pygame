import socket
from _thread import *
import pickle
import random 
from components import *

server = "localhost"
port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    #if data == "reset":
                    #    print("oi")
                    if data != "get":
                        print(f"different data: {data}")
                        game.shoot(p, data)
                        print(f"atirei")

                    print(game)
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        games[gameId].players[p] = Player()
        games[gameId].current_player_id = p
        print("Creating a new game...")
    else:
        p = 1
        games[gameId].players[p] = Player()
        games[gameId].ready = True


    start_new_thread(threaded_client, (conn, p, gameId))