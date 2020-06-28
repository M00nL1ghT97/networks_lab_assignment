import socket
import threading
from random import randint

class Server():

    def __init__(self):
        print("Server init")
        self.sock, self.server_addr = self.create_server_socket()
        while self.sock is None:
            self.sock, self.server_addr = self.create_server_socket()
        self.clients = []
        self.lock = threading.Lock()

    def shutdown(self):
        with self.lock:
            for s in self.clients:
                s.close()
            self.clients = []
        self.sock.close()

    def start(self):
        threading.Thread(target=self.accepting_on_server_socket).start()
        print("server start "+str(self.server_addr))
        return self.server_addr

    def create_server_socket(self):
        res = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = ("localhost", randint(10000, 15000))
        try:
            res.bind(server_addr)
            res.listen(10)
            return res, server_addr
        except:
            return None, None
        
    def accepting_on_server_socket(self):
        while True:
            try:
                sock, client_addr = self.sock.accept()
            except:
                print("Closing main socket")
                break
            with self.lock:
                self.clients.append(sock)
                t = threading.Thread(target=self.serve_a_client, args=(sock,))
                t.start()
        
    def serve_a_client(self, sock):
        while True:
            try:
                message = sock.recv(1024).decode("utf-8")
            except:
                print("Closing connection")
                break

            # if message is quit then 
            if message=="quit":
                with self.lock:
                    self.clients.remove(sock)
                    break
            else:
                with self.lock:
                    message = str(self.server_addr)+ " - "+message
                    print(message)
                    for s in self.clients:
                        if s != sock:
                            try:
                                s.sendall(message.encode("utf-8"))
                            except:
                                pass