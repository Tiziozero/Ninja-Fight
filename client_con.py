import socket
import pickle
import threading

from error_log import eprint

class Network:
    def __init__(self, ip_address, port):
        self.addr = ip_address
        self.port = port
        self.network = socket.socket()
        # self.network.bind((self.addr, self.port)) 
        self.network.connect((self.addr, self.port))
        self.connection_data = pickle.loads(self.network.recv(1024))
        print(self.connection_data)
        self.connection_data1 = pickle.loads(self.network.recv(1024))
        print(self.connection_data1)
        self.ongoing = True
        self.server_connected = True

    def run(self):
        print("game run")
        self.recv_thread = threading.Thread(target=self.recv, args=())
        # self.send_thread = threading.Thread(target=self.send, args=())
        self.recv_thread.start()
        # self.send_thread.start()

    def send(self):
        return
        send_data = input("send data: ")
        while self.ongoing and self.server_connected:
            try:
                data = self.network.send(picke.dumps(send_data))
                print("data: {data}")
            except socket.error as e:
                eprint(e)
            except pickle.UnpicklingError as e:
                eprint(e)
            except:
                eprint("Unknown Error.")
    def recv(self):
        while True:
            try:
                print(pickle.loads(self.network.recv(1024)))
            except:
                print("eee")
if __name__ == '__main__':
    n = Network('localhost', 48872)
    n.run()
