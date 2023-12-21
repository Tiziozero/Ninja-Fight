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
                self.games.append(game_session)

        except socket.error as e:
            server_log("Socket error", level=1)
            eprint(e)
            # Consider adding cleanup or reinitialization here
        except KeyboardInterrupt:
            server_log("KeyboardInterrupt. Server forcefully closed.", level=0)
        finally:
            for g in self.games:
                g.server_close()
            self.server.close()
            server_log("Closed server", level=1)

class Con:
    def __init__(self, entity_id, conn, addr, game):
        self.id = entity_id
        self.conn = conn
        self.addr = addr
        self.game = game

class Game_Session_Server:
    def __init__(self, conn, addr, conn2, addr2):
        self.c1 = Con(69348878, conn, addr, self)
        self.c2 = Con(69348879, conn2, addr2, self)
        self.server_id = 69420
        self.connections = []
        self.connections.append(self.c1)
        self.connections.append(self.c2)
        self.data = "hello client"
        self.server_on = True


        startup_thread =  threading.Thread(target=self.run, args=())
        startup_thread.start()
    def run(self):
        print(f"started server {self.server_id}")
        recv_thread_1 = threading.Thread(target=self.recv, args=(self.c1,))
        recv_thread_1.start()
        send_thread_1 = threading.Thread(target=self.send, args=(self.c1, "Hello world!",))
        recv_thread_2 = threading.Thread(target=self.recv, args=(self.c2,))
        recv_thread_2.start()
        send_thread_2 = threading.Thread(target=self.send, args=(self.c2, "Hello world!",))
        recv_thread_1.join()
        recv_thread_2.join()
        self.server_close()
        

    def send(self, con, data):
        return
        while self.server_on:
            try:
                con.conn.send(pickle.dumps(data))
            except socket.error as e:
                eprint(e)
                self.server_on = False
                break
            except pickle.UnpicklingError as e:
                eprint(e)
                self.server_on = False
                break
            except EOFError as e:
                eprint(e)
                self.server_on = False
                break
            except BrokenPipeError as e:
                eprint(e)
                self.server_on = False
                break
            except ConnectionAbortedError as e:
                eprint(e)
                self.server_on = False
                break
            except ConnectionResetError as e:
                eprint(e)
                self.server_on = False
                break
            except:
                eprint("Unknown error.")
                self.server_on = False
                break


    def recv(self, con):
        while self.server_on:
            try:
                data = pickle.loads(con.conn.recv(1024))
                print(f"Game: {str(self.server_id): <10}; Connection: {str(con.addr): <25}: Data: {data}")
            except socket.error as e:
                eprint(e)
                self.server_on = False
                break
            except pickle.UnpicklingError as e:
                eprint(e)
                self.server_on = False
                break
            except EOFError as e:
                eprint(e)
                self.server_on = False
                break
            except BrokenPipeError as e:
                eprint(e)
                self.server_on = False
                break
            except ConnectionAbortedError as e:
                eprint(e)
                self.server_on = False
                break
            except ConnectionResetError as e:
                eprint(e)
                self.server_on = False
                break
            except:
                eprint("Unknown error.")
                self.server_on = False
                break
        server_log(f"ID: {self.server_id}: server_on is False")
        return

    def server_close(self):
        self.server_on = False
        for c in self.connections:
            c.conn.close()
        server_log(f"Closed server {self.server_id}.")
if __name__ == '__main__':
    print("Runiong")
    server_class = Server("localhost", 48878)
    server_class.run()
