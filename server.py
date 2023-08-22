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
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            kill_process_on_port(port)
        except:
            pass
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
        addr, username = self.clients[client]
        try:
            while True:
                data = client.recv(1024)
                if not data:  # client disconnected
                    break
                self.broadcast(data, client)
        except:
            pass
        finally:
            client.close()
            del self.clients[client]
            print(f"{username} {addr} disconnected")


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
