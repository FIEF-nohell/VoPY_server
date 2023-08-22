import socket
from threading import Thread

class Server:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = {}

    def broadcast(self, data, source):
        for client, addr in self.clients.items():
            if client != source:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self, client):
        while True:
            try:
                data = client.recv(1024)
                self.broadcast(data, client)
            except:
                pass

    def run(self):
        print("Server started...")
        while True:
            client, addr = self.server.accept()
            print(f"Connected with {addr}")
            self.clients[client] = addr
            thread = Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = Server("0.0.0.0", 12345)
    server.run()
