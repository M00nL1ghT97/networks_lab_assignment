import socket
import threading

COORDINATOR_ADDRESS = ("localhost", 7777)

class Client():

    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def create_session(self, session_name):
        message = "create "+session_name
        self.udp_socket.sendto(message.encode("utf-8"), COORDINATOR_ADDRESS)
        data, _ = self.udp_socket.recvfrom(1024)
        print(data)

    def join_session(self, session_name):
        message = "join "+session_name
        self.udp_socket.sendto(message.encode("utf-8"), COORDINATOR_ADDRESS)
        data, _ = self.udp_socket.recvfrom(1024)
        message = data.decode("utf-8")

        if message[0]=="N":
            print(message)
        else:
            message = message.replace(" ","")
            message = message.replace("'","")
            message = message.replace("(","")
            message = message.replace(")","")
            a,b = message.split(",")
            addr = (a, int(b))
            self.connect_to_server(addr)

    def leave_session(self):
        self.tcp_socket.close()
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self, addr):
        self.tcp_socket.connect(addr)
        threading.Thread(target=self.listen_to_tcp_socket).start()

    def listen_to_tcp_socket(self):
        while True:
            try:
                message = self.tcp_socket.recv(1024).decode("utf-8")
            except:
                print("broken tcp connection")
                break
            print(message)
    
    def send_message(self, message):
        self.tcp_socket.sendall(message.encode("utf-8"))
