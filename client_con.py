import socket
import pickle
import threading
from error_log import eprint

class Network:
    def __init__(self, ip_address, port, player=None):
        self.addr = ip_address
        self.port = port
        self.network = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.conn_on = True
        self.server_connected = True
        self.data = 'no data'

    def setup(self):
        # Send a request to the server
        self.network.sendto(pickle.dumps("Request"), (self.addr, self.port))

        # Corrected typo in 'recvfrom' and removed unnecessary tuple
        data, _ = self.network.recvfrom(1024)  # 1024 is the buffer size
        data = pickle.loads(data)
        print(data)
        self.port = int(data["port"])
        print(f"Address: {self.addr}, Port: {self.port}")

        r_thread = threading.Thread(target=self.recv, args=())
        s_thread = threading.Thread(target=self.send, args=())
        r_thread.daemon = True
        s_thread.daemon = True
        r_thread.start()
        s_thread.start()

    def recv(self):
        while self.conn_on:
            try:
                data, _ = self.network.recvfrom(1024)
                data = pickle.loads(data)
                print(data)
            except Exception as e:
                eprint(f"recv: {e}")
                # self.conn_on = False
                # break
    def send(self):
        while self.conn_on:
            try:
                self.network.sendto(pickle.dumps("data"), (self.addr, int(self.port)))
            except Exception as e:
                eprint(f"send: {e}")
                self.conn_on = False
                break

if __name__ == '__main__':
    n = Network('localhost', 48878)
    Network.setup(n)
    input("Enter to set conn_on to False.")
    n.conn_on = False
    input("Enter to end programm.")
