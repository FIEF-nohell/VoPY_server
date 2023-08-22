import socket
from threading import Thread

class Server:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = {}

if __name__ == "__main__":
    server = Server("0.0.0.0", 12345)
    server.run()