from server import Server
import threading, socket

class Coordinator():
    def __init__(self, addr):
        self.session_register = {}
        self.lock = threading.Lock()
        self.udp_socket = self.create_udp_socket(addr)
        self.serve_socket()

    def create_udp_socket(self, addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(addr)
        return s

    def serve_socket(self):
        while True:
            data, addr = self.udp_socket.recvfrom(1024)
            message = data.decode("utf-8").lower()
            command, session_name = message.split(" ")
            if command == "create":
                self.create_session(addr, session_name)
            elif command == "close":
                self.delete_ssession(addr, session_name)
            elif command == "join":
                self.join_session(addr, session_name)
            else:
                self.udp_socket.sendto("Not valid request".encode("utf-8"), addr)

    def create_session(self, addr, session_name):
        server = Server()
        session_addr = server.start()
        with self.lock:
            self.session_register[session_name] = (addr, server, session_addr)
        self.udp_socket.sendto(str(session_addr).encode("utf-8"), addr)

    def delete_ssession(self, addr, session_name):
        if self.session_register[session_name][0]==addr:
            with self.lock:
                self.session_register[session_name].shutdown()
                del self.session_register[session_name]
            self.udp_socket.sendto("Success".encode("utf-8"), addr)
        else:
            self.udp_socket.sendto("You are not the owner".encode("utf-8"), addr)

    def join_session(self, addr, session_name):
        with self.lock:
            if session_name in self.session_register:
                session_addr = self.session_register[session_name][2]
                self.udp_socket.sendto(str(session_addr).encode("utf-8"), addr)
                return
        self.udp_socket.sendto("No such session found".encode("utf-8"), addr)
        
        
