import socket
import pickle
import threading
from error_log import eprint
vlog = 0
try:
    vlog = int(input("server log level [-1(None) - 5(All)] (default 0): "))
except:
    print("Invalid inpur. vlog set to 0")

def server_log(text, level=0, end=None):
    if vlog >= level:
        for i in range(level): print("\t", end='')
        print(f"Srver Log: {text}", end=end)

class Server:
    def __init__(self, ip_address, port):
        self.addr = ip_address
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.addr, self.port))
        self.server.listen()
        self.games = []

   def run(self):
        try:
            server_log("Running...")
            while True:
                server_log("waiting for clients...")
                conn, addr = self.server.accept()
                server_log(f"Accepted connection from {conn}, {addr}")
                conn.send(pickle.dumps("player 1"))

                conn2, addr2 = self.server.accept()
                server_log(f"Accepted connection from {conn2}, {addr2}")
                conn2.send(pickle.dumps("player 2"))

                conn.send(pickle.dumps("game_start"))
                conn2.send(pickle.dumps("game_start"))

                game_session = Game_Session_Server(conn, addr, conn2, addr2)
                game_session.setup()
                self.games.append(game_session)

        except socket.error as e:
            server_log("Socket error", level=1)
            eprint(e)
            # Consider adding cleanup or reinitialization here
        except KeyboardInterrupt:
            server_log("KeyboardInterrupt. Server forcefully closed.", level=0)
        finally:
            self.server.close()
            server_log("Closed server", level=1)
class Game_Session_Server:
    def __init__(self, conn, addr, conn2, addr2):
        self.c1 = conn
        self.c2 = conn2

    def setup(self):
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.start()

    def sendall(self, data):
        try:
            data = pickle.dumps(data)
            self.c1.send(data)
            self.c2.send(data)
        except:
            eprint("idk  something")
    def run(self):
        print("Running server")
        while True:
            try:
                sendall("hello, client")
                print("send data")
            except:
                pass


if __name__ == '__main__':
    print("Runiong")
    server_class = Server("localhost", 48872)
    server_class.run()
