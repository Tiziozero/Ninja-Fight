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
        self.data = 'no data'

    def run(self):
        print("game run")
        self.recv_thread = threading.Thread(target=self.recv, args=())
        self.send_thread = threading.Thread(target=self.send, args=())
        self.recv_thread.start()
        self.send_thread.start()

    def send(self):
        while self.ongoing and self.server_connected:
            print("yess")
            try:
                send_data = input("send data: ")
                if send_data == 'quit':
                    self.close()
                    break
                self.network.send(pickle.dumps(send_data))
                print("data: {data}")
            except socket.error as e:
                eprint(e)
            except pickle.UnpicklingError as e:
                eprint(e)
            #except Keyboardinterrupt as e:
            #    eprint(e)
            #    self.close()
            except:
                eprint("Unknown Error.")
    def recv_data(self):
        try:
            data = self.network.recv(1024)
            if data == b'':
                eprint("Connection closed by the remote host.")
                return None
            return pickle.loads(data)
        except socket.error as e:
            eprint(e)
        except pickle.UnpicklingError as e:
            eprint(e)
        except EOFError as e:
             eprint(e)
        except BrokenPipeError as e:
            eprint(e)
        except ConnectionAbortedError as e:
            eprint(e)
        except ConnectionResetError as e:
            eprint(e)
        except Exception as e:  # Using a generic exception is not best practice
            eprint(f"Unknown error: {e}")
        return 'no data'


    def recv(self):
        return
        while True:
            try:
                data = pickle.loads(self.network.recv(1024))
                return data
            except socket.error as e:
                eprint(e)
            except pickle.UnpicklingError as e:
                eprint(e)
            except:
                eprint("Unknown Error.")
    def close(self):
        self.ongoing = False
        self.network.close()
        print("Closed network.")
if __name__ == '__main__':
    n = Network('localhost', 48878)
    Network.run(n)
