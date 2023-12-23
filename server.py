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
        # UDP Socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.addr, self.port))
        self.games = []

    def listen(self):
        try:
            current_port = 3535  # Initial game session port
            current_id = 69420
            server_log("Running...")
            while True:
                server_log("waiting for clients...")
                game_port = current_port
                current_port += 1
                game_id = current_id
                current_id += 1

                # Receive requests from two clients
                request, conn1 = self.server.recvfrom(1024)
                server_log(f"Received request from {conn1}")
                data = {"port": game_port, "player": 1}
                self.server.sendto(pickle.dumps(data), conn1)
                
                request, conn2 = self.server.recvfrom(1024)
                server_log(f"Received request from {conn2}")
                data = {"port": game_port, "player": 2}
                self.server.sendto(pickle.dumps(data), conn2)
                # make an imaginary thread that keeps connections alive while waiting for the second client

                # Increment the port for a new game session

                # Create and start a new game session
                game_session = Game_Session_Server(game_id, game_port, self.addr, conn1, conn2)
                self.games.append(game_session)
        except socket.error as e:
            server_log("Socket error", level=1)
            eprint(e)
        except KeyboardInterrupt:
            server_log("KeyboardInterrupt. Server forcefully closed.", level=0)
        finally:
            # Close all game sessions and the server
            for g in self.games:
                g.server_close()
            server_log("Closed server", level=1)
            self.server.close()

class Con:
    def __init__(self, entity_id, conn, game):
        self.id = entity_id
        self.conn = conn
        self.game = game

class Game_Session_Server:
    def __init__(self, game_id, game_port, game_addr, conn, conn2):
        self.game_port = game_port
        self.game_addr = game_addr
        server_log(f"addr: {str(self.game_addr): >30}; port: {str(self.game_port): >30}")

        try:
            self.game_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.game_server.bind((self.game_addr, self.game_port))
            self.game_id = game_id
        except Exception as e:
            eprint(e)

        self.c1 = Con(69348878, conn, self)
        self.c2 = Con(69348879, conn2, self)

        self.connections = []
        self.connections.append(self.c1)
        self.connections.append(self.c2)
        self.data = 0

        self.server_on = True
        startup_thread =  threading.Thread(target=self.run, args=())
        startup_thread.start()

    def run(self):
        self.game_server.sendto(pickle.dumps("data"), self.c1.conn)
        self.game_server.sendto(pickle.dumps("data"), self.c2.conn)
        for g in self.connections:
            g_thread = threading.Thread(target=self.handle_conn, args=(g,))
            g_thread.start()

    def handle_conn(self, conn):
        send_thread = threading.Thread(target=self.send, args=(conn,))
        recv_thread = threading.Thread(target=self.recv, args=(conn,))
        send_thread.daemon = True
        recv_thread.daemon = True
        send_thread.start()
        recv_thread.start()

    def send(self, conn):
        return
        server_log(f"sending from server: {self.game_id}")
        while self.server_on:
            try:
                self.game_server.sendto(pickle.dumps("data"), conn.conn)
            except Exception as e:
                eprint(e)
    def recv(self, conn):
        server_log(f"receiving from server: {self.game_id}")
        while self.server_on:
            try:
                data, _ = self.game_server.recvfrom(1024)
                data = pickle.loads(data)
            except Exception as e:
                eprint(e)
    
    def server_close(self):
        pass

if __name__ == '__main__':
    print("Runiong")
    server_class = Server("localhost", 48878)
    server_class.listen()
