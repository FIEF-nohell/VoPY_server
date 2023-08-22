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
        ...
        self.frequencies = {str(i): [] for i in range(1, 10)}

    def broadcast(self, data, source, frequency):
        for client in self.frequencies[frequency]:
            if client != source:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self, client):
        username = client.recv(1024).decode('utf-8')
        frequency = client.recv(1024).decode('utf-8')
        
        self.frequencies[frequency].append(client)
        
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                self.broadcast(data, client, frequency)
            except:
                pass

    def run(self):
            print("Server started...")
            while True:
                client, addr = self.server.accept()
                username = client.recv(1024).decode('utf-8')
                print(f"{username} connected with {addr}")
                self.clients[client] = (addr, username)
                thread = Thread(target=self.handle_client, args=(client,))
                thread.start()

if __name__ == "__main__":
    server = Server("0.0.0.0", 12345)
    server.run()
