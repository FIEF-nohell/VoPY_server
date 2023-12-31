from threading import Thread
import subprocess
import socket
import os

def kill_process_on_port(port):
    cmd = f'netstat -ano | findstr :{port}'
    result = subprocess.check_output(cmd, shell=True).decode('cp1252')
    lines = result.strip().split("\n")
    pids = [line.split()[-1] for line in lines]

    for pid in pids:
        print("Attempting to kill process", pid)
        os.system(f'taskkill /F /PID {pid}')

class Server:
    def __init__(self, host, port):
        # Initialize the server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # This allows the address/port to be reused immediately instead of it being stuck in the TIME_WAIT state waiting for late packets to arrive.
        self.server.bind((host, port))
        self.server.listen(5)  # Allow up to 5 pending connections

        self.frequencies = {str(i): [] for i in range(1, 10)}
        self.clients = {}  # This dictionary will store client socket objects and their associated address and username.

    def broadcast(self, data, source, frequency):
        for client in self.frequencies[frequency]:
            if client != source:
                try:
                    client.send(data)
                except:
                    pass

    def run(self):
        print("Server started...")
        while True:
            client, addr = self.server.accept()
            thread = Thread(target=self.handle_client, args=(client, addr))
            thread.start()

    def handle_client(self, client, addr):
        try:
            frequency = client.recv(1024).decode('utf-8')
            print("\nIncoming connection request on frequency: " + str(frequency))
            username = client.recv(1024).decode('utf-8')
            print("Incoming connection request from username: " + str(username))
        except UnicodeDecodeError:
            print("Received unexpected data from client. Disconnecting client.")
            client.close()
            return

        print(f"{username} connected with {addr}")

        # Validate the frequency
        if frequency not in self.frequencies:
            print(f"Invalid frequency received: {frequency}. Disconnecting client.")
            client.close()
            return

        self.clients[client] = (addr, username)
        self.frequencies[frequency].append(client)
            
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                self.broadcast(data, client, frequency)
            except:
                pass


if __name__ == "__main__":
    server = Server("0.0.0.0", 12345)
    server.run()